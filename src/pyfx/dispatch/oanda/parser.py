# origianlly tokenize-ijson.py - tokenization tests for an application of ijson

from abc import abstractmethod, ABC
import asyncio as aio
import concurrent.futures as cofutures
import inspect
import ijson
import logging
import os

from typing import Any, AsyncGenerator, Callable, Generic, Mapping, Optional, Self, Sequence, Union
from typing_extensions import Generic, TypeVar

from .io import AsyncSegmentChannel, DataError
from .transport import (   # type: ignore
    ApiObject, AbstractApiObject, AbstractApiClass, ApiClass,
    TransportFieldInfo, TransportType, TransportValues, JsonTypesRepository
)
from .response_common import ResponseInfo
from .exceptions import ApiException
from .response_common import REST_CONTENT_TYPE
from .exec_controller import ExecController, thread_loop


class NoResponse(DataError):
    pass

##
## The builder model for applying ijson with the ApiObject model
##


T = TypeVar("T")
Tmodel = TypeVar("Tmodel", bound=ApiObject)

logger: Optional[logging.Logger] = logging.getLogger(__name__) if __debug__ else None

MODEL_BUILDER_DEBUG: bool = "MODEL_BUILDER_DEBUG" in os.environ if __debug__ else False


def model_builder_debug(fmt, *args):
    if MODEL_BUILDER_DEBUG:
        logger.debug(fmt, *args)


class InstanceBuilder(Generic[T], ABC):
    '''Specialization of the ijson ObjectBulder pattern, for ApiObject deserialization'''

    __slots__ = ("instance_class", "instance", "origin", "builder", "finalized", "key")

    instance_class: Optional[type[Tmodel]]  # type: ignore
    '''
    Instance class expected for deserialization with this builder

    This value may be None when parsing a mapping under an unrealized abstract type
    '''

    instance: Tmodel  # type: ignore
    '''Reference for the deserialized instance, during deserialization'''

    key: Optional[str]
    '''Current key to be deserialized, for mapping values'''

    origin: Optional["InstanceBuilder"]
    '''The containing builder, if any'''

    builder: Union["InstanceBuilder" | Self]
    '''The next builder for event forwarding, or this instance itself'''

    finalized: bool
    '''Flag for indicating whether the builder has reached end-of-object in the input stream'''

    def finalize(self):
        # proto may be a mapping object, mainly when deserializing
        # an abstract API object type
        proto = self.instance
        # set the finalized prototype object as the instance
        model_cls = self.instance_class
        if model_cls:
            # ensure any abstract type is realized
            #
            # if not reached, it's assumed that the mapping will be realized
            # when the containing abstract type is realized
            self.instance = model_cls.finalize_prototype(proto)
        self.finalized = True

    def __init__(self, cls: Optional[type], origin: "Optional[InstanceBuilder]" = None):
        super().__init__()
        self.builder = self
        self.origin = origin  # the containing builder, if any
        # self.instance = None
        self.instance_class = cls
        self.finalized = False
        self.key = None

    @abstractmethod
    def instance_prototype(self) -> T:
        raise NotImplementedError(self.instance_prototype)

    @abstractmethod
    async def aevent(self, event: str, value: Any, async_callback=None):
        raise NotImplementedError(self.aevent)

    def __repr__(self):
        return "<%s [%s] at 0x%x>" % (self.__class__.__name__, self.instance_class.__name__, id(self),)


class ModelBuilder(InstanceBuilder[Tmodel], Generic[Tmodel]):
    __slots__ = tuple(set(InstanceBuilder.__slots__).union({"api_fields", "designator_key", "realize_abstract"}))

    api_fields: Mapping[str, TransportFieldInfo]
    """
    Mapping of field names and field alias names to field information objects
    for the instance class.

    In the API for fxTrade v20, every field in this table will be a
    TransportFieldInfo object, containing additional fields and
    member functions for the parse. This class is a subclass of Pydantic
    FieldInfo.

    This slot is initialized from the api_fields field on the
    instance class for the builder.
    """

    designator_key: Optional[str]
    """
    Storage for the designator key when initializing an abstract API object.

    This value will be None when initializing a concrete API object. Else, the
    value will provide the key name for the designator key of the abstract API
    object.
    """

    realize_abstract: bool
    """
    Indicator flag for abstract instance initialization.

    This value will be set to True when the designator_key is parsed,
    on the assumption that the next parser event will provide the
    value for the designator key.
    """

    def __init__(self, cls: Optional[type[ApiObject]], origin: Optional[InstanceBuilder] = None):
        ## the model class `cls` should be provided at a top level. The value may be None
        ## when parsing a mapping under an unrealized abstract type
        self.realize_abstract = False
        if isinstance(cls, AbstractApiClass):
            # cls: type[AbstractApiObject]
            self.designator_key = cls.designator_key
        else:
            self.designator_key = None
        super().__init__(cls, origin)
        self.api_fields = cls.api_fields if cls else None

    def instance_prototype(self) -> ApiObject:
        # generally called only when self.key is None and self.instance is unset
        #
        # when self.key is not none, the processing would be fowarded to a next builder
        #
        # when parsing under an unrealized abstract type, returns a generic dict
        key = self.key
        cls: type[ApiObject] = self.instance_class if key is None else self.get_field_transport_type(key).storage_class  # type: ignore
        if __debug__:
            model_builder_debug("%s instance_prototype: create %s", self.__class__.__name__, cls.__name__ if cls else "<Abstract>")
        return cls.create_prototype() if cls else {}

    def get_storage_key(self, key: str) -> str:
        # api_fields may be None when parsing under an unrealized abstract type
        fields = self.api_fields
        if fields and key in fields:
            return fields[key].field_name
        elif isinstance(self.instance, Mapping):
            # parsing an abstract type
            return key
        else:
            ## in this implementation, every field needs to be annoted with TransportFieldInfo,
            ## such that the field information would provide the original field name
            raise ValueError("Not a supported model key", key, self.instance_class)

    def get_field_transport_type(self, key: str) -> Optional[TransportType]:
        # may return None during 'start_map' under an unrealized abstract type
        fields = self.api_fields
        if fields and key in fields:
            field = fields[key]
            if isinstance(field, TransportFieldInfo):
                cls = field.transport_type
                assert cls, "Field has a null storage class"
                return cls
            else:
                # Pseudocode for generalized applications onto pydantic
                #
                # Untested, this endeavors to provide a certain degree of
                # portability for FieldInfo definitions not caching any
                # internal transport type
                #
                # The transport type determined here should provide parse()
                # as a class method, accepting the corrresponding value
                # as decoded by the ijson/yajl parser
                #
                # This is semantically similar to the handling for
                # TransportFieldInfo fields. In this section, the
                # transport type for the field would not be determined
                # until parse.
                #
                annot = field.annotation
                if not annot:
                    raise ValueError("Field is not annotated", key, self.instance_class)
                cls = JsonTypesRepository.get_transport_type(annot)
                if cls:
                    return cls
                else:
                    raise ValueError("No type class found", key, annot, self.instance_class)
        elif not self.instance_class or issubclass(self.instance_class, AbstractApiObject):
            return None
        else:
            raise ValueError("Unknown field", key, self.instance_class, set(fields.keys()), self.instance)

    def set_field(self, value: Any):
        key: str = self.key  # type: ignore
        if isinstance(self.instance, ApiObject):
            # when not deferring initialization with a dict mapping,
            # ensure field tracking for applications onto Pydantic
            self.instance.model_fields_set.add(key)
            # using object.__setattr__ to avoid pydantic's model field validation
            #
            # Known Limitation: This assumes that the data being parsed is from a
            # trusted provider and would be valid for the containing model field
            return object.__setattr__(self.instance, key, value)
        else:
            # assumption: self.instance is a dictionary, or a dict-like  object
            # such that can be accessed with a string subscript
            self.instance[key] = value  # type: ignore

    def realize_instance(self, type):
        # utility method for application when parsing an abstract API object type
        inst = self.instance_class.realize_map(type, self.instance)
        concrete_cls = inst.__class__
        self.instance_class = concrete_cls
        self.api_fields = concrete_cls.api_fields
        self.instance = inst
        # print("XREIF " + repr(inst))
        self.realize_abstract = False

    async def aevent(self, event: str, value: Any, async_callback=None):
        # An implementation after ijson.ObjectBuilder.event() as a driver
        # for the ijson tokenizer => builder cycle - generalized mainly
        # for the ApiObject class provided to this builder's constructor,
        # furthermore defined as an async method
        #
        # An application is illustrated together with the segment channel
        # stream interface, in cls.from_string_async()
        builder = self.builder
        if builder is self:
            if __debug__:
                model_builder_debug("ModelBuilder: event %s %s (%s)", self.key, event, self.instance_class.__name__ if self.instance_class else "<Abstract>")
            match event:
                case "start_map":
                    key = self.key
                    if key is None:
                        ## ensure that this builder's primary instance is created
                        ## for per-field initialization during the parse
                        if not hasattr(self, "instance"):
                            if __debug__:
                                model_builder_debug("Create primary instance, %s", self.instance_class.__name__ if self.instance_class else "<Abstract>")
                            self.instance = self.instance_prototype()
                    else:
                        # create a new model builder for event forwarding at start_map
                        #
                        # mtyp may be none when parsing a mapping under an unrealized abstract type
                        mtyp = self.get_field_transport_type(key)
                        proto_cls: type[ApiObject] = mtyp.storage_class if mtyp else None
                        builder = self.__class__(proto_cls, self)
                        self.builder = builder
                        await builder.aevent(event, value)

                case 'end_map':
                    # Implementation Note:
                    # Using one model builder per top-level element,
                    # streaming or otherwise in the reader protocol
                    if __debug__:
                        model_builder_debug("Finalizing %r", self.instance)
                    self.finalize()
                    if async_callback:
                        if __debug__:
                            model_builder_debug("Dispatch to callback for %r", self.instance)
                        await async_callback(self.instance)
                    return
                case 'map_key':
                    try:
                        self.key = self.get_storage_key(value)
                    except ValueError as exc:
                        if value == self.designator_key:
                            # Assumption: the next parser event should provide
                            # the value for the designator key
                            self.realize_abstract = True
                            self.key = value
                        else:
                            raise
                case 'start_array':
                    # create a new sequence builder for event forwarding
                    #
                    # this assumes that the containing field is decribed with
                    # a values-typed field info instance, such that the internal
                    # member class for the field is represented in the provided
                    # field info
                    inst_cls = self.instance_class
                    ## field may be null when parsing a mapping under an unrealized abstract type
                    field: TransportFieldInfo = inst_cls.api_fields.get(self.key, None) if inst_cls else None  # type: ignore
                    member_transport: TransportValues = field.transport_type if field else None
                    builder = SequenceBuilder(member_transport, self)
                    self.builder = builder
                    await builder.aevent(event, value)
                case 'end_array':
                    seq = builder.instance
                    self.set_field(tuple(seq))
                    self.builder = self
                case 'string':
                    if self.realize_abstract:
                        self.realize_instance(value)
                    transport = self.get_field_transport_type(self.key)  # type: ignore
                    parsed = None
                    if __debug__:
                        # the transport type may not be known when parsing a mapping
                        # under an unrealized abstract type
                        if transport and not isinstance(transport, type):
                            raise AssertionError("Not a class", transport, self.key, self.instance_class, self.instance)
                    if transport is None:
                        # deferring deserialization
                        parsed = value
                    elif issubclass(transport, TransportType) or isinstance(transport, TransportType):
                        parsed = transport.parse(value)
                    else:
                        raise ValueError("Not a transport type", transport)
                        # parsed = cls(value)
                    self.set_field(parsed)
                case _:
                    self.set_field(value)
        else:
            # dispatch to the forwarded builder
            await builder.aevent(event, value)
            if builder.builder is builder:
                # process the builder for finalization
                match event:
                    case 'end_map' | 'end_array':
                        if builder.finalized:
                            self.set_field(builder.instance)
                            del builder
                            self.builder = self

    @classmethod
    async def from_text_async(cls, model_cls: type[Tmodel], data: Union[bytes, str],
                              loop: Optional[aio.AbstractEventLoop] = None) -> Tmodel:
        async with AsyncSegmentChannel(loop=loop or aio.get_running_loop()) as stream:
            await stream.feed(data, True)
            builder = cls(model_cls)
            async for event, value in ijson.basic_parse_async(stream, use_float=True):
                await builder.aevent(event, value)
            return builder.instance

    @classmethod
    def from_text(cls, model_cls: type[Tmodel], data: Union[bytes, str]) -> Tmodel:
        loop = aio.get_event_loop_policy().get_event_loop()
        return loop.run_until_complete(cls.from_text_async(model_cls, data))

    @classmethod
    async def from_response_async(cls, response_info: ResponseInfo,
                                  stream: AsyncSegmentChannel,
                                  model_cls_callback: Callable[[ResponseInfo, bytes], Optional[type[ApiObject]]],
                                  model_callback: Callable[[ApiObject], Any]
                                  ):

        response_map = response_info.response_types_map
        status = response_info.status
        content_type = response_info.content_type

        content_encoding = response_info.content_encoding

        loop = aio.get_running_loop()

        async def callback_wrapper(result: ApiObject):
            ## Implementation Note: ModelBuilder.event() is implemented
            ## in the ijson base class as a synchronous function.
            ##
            ## By extension, event() is defined here and called as a
            ## coroutine function. As such, this callback wrapper can
            ## be provided to the function as a coroutine without
            ## additional task/gather=>future scheudling
            ##
            ## Albeit, this may not scale particularly well for
            ## multi-threaded applications
            nonlocal model_callback, stream
            await stream.aclose()
            if inspect.iscoroutinefunction(model_callback):
                await model_callback(result)
            else:
                model_callback(result)

        ## if the status is found in the response_map at this point, it probably
        ## indicates an error response from the server
        model_cls = response_map[status] if status in response_map else None

        ## retrieve the next chunk for parsing, without advancing stream cursor
        chunk: bytes = stream.next_chunk()

        if content_type != REST_CONTENT_TYPE:
            ## the Api Client may have received an intermediate proxy
            ## response. raise and return
            ##
            ## Known Limitation: this may serve to embed a proxy response
            ## page within the exception message. Applications may be able
            ## to unparse this content into a meaningful representation,
            ## when handling the exception.
            ##
            # fmt: off
            response_text = chunk.decode(content_encoding) if content_encoding else chunk.decode()
            raise ApiException(status=status, reason=response_info.reason,
                               response=response_text, content_type = content_type)  # type: ignore
            # fmt: on
        elif status > 299:
            ## as one convention in the fxTrade v20 API, every streaming 'success'
            ## response uses 200 as a response code. Other codes would indicate
            ## some issue in the request/response chain
            ##
            ## here: read the server error response, raise Api Exception
            model_cls = model_cls_callback(response_info, chunk)
            exc_response = None
            if model_cls:
                ## the response represents an expected response for the
                ## related endpoint
                builder: ModelBuilder = cls(model_cls)
                # fmt: off
                async for event, value in ijson.basic_parse_async(stream, use_float=True):
                    await builder.aevent(event, value)
                # fmt: on
                exc_response = builder.instance
            else:
                async for toplevel in ijson.items(stream, ''):
                    ## parse what should be a single toplevel JSON object
                    ##
                    ## here, the response object will be presented to the
                    ## caller typically as a partially parsed mapping object
                    ##
                    ## e.g for "temporary redirect" with a response code 307,
                    ## seen when the client did not have redirects enabled
                    exc_response = toplevel
                    break
            ## raise the parsed exception
            # fmt: off
            raise ApiException(status=status, reason=response_info.reason,
                               response=exc_response)  # type: ignore
            # fmt: on

        ## main parsing for the streaming response
        while not stream.closed():
            model_cls = model_cls_callback(response_info, chunk)
            ## None from model_cls_callback indicates "skip"
            if not model_cls:
                continue

            # assert not stream.closed(), "stream closed before segment read"

            if model_cls:
                ## constructing a new ModelBuilder for each chunk,
                ## assuming each chunk represents a completely encoded
                ## JSON object to be decoded for a single type, with
                ## that type generally determined per the client/server
                ## request protocol
                builder = cls(model_cls)
                async for event, value in ijson.basic_parse_async(stream, use_float=True):
                    ## Implementation Note: This is where the main parser runs ...
                    await builder.aevent(event, value, callback_wrapper)
            else:
                ## generic read - unexpected value, read the chunk then break
                unexpected = None
                async for toplevel in ijson.items(stream, ''):
                    unexpected = toplevel
                    break
                await stream.feed('', True)  # indicate EOF in the stream
                raise ApiException(status=0, reason="Parser: Unexpected value",
                                   response=unexpected)  # type: ignore

    @classmethod
    async def from_receiver_gen(cls, controller: ExecController,
                                model_cls_callback: Callable[[ResponseInfo, bytes], Optional[type[ApiObject]]],
                                model_callback: Callable[[ApiObject], Any],
                                loop: Optional[aio.AbstractEventLoop] = None
                                ) -> AsyncGenerator[ApiObject, Union[ResponseInfo, bytes, None]]:
        ## read a server response from an fxTrade v20 streaming endpoint,
        ## via async generator.
        ##
        ## This generator will be provided to the REST client, which will feed
        ## a sequence of byte chunks, each generally containing a complete
        ## JSON string or a complete non-JSON response
        async with AsyncSegmentChannel[bytes](loop = loop or aio.get_running_loop()) as stream:
            response_info: ResponseInfo = yield  # type: ignore
            if __debug__:
                model_builder_debug("from_receiver_gen: Received response info %r", response_info)

            assert isinstance(response_info, ResponseInfo), "Received unexpected value"

            def parse_response():
                nonlocal cls, response_info, stream, model_cls_callback, model_callback
                global thread_loop
                loop = thread_loop.get()
                coro = cls.from_response_async(response_info, stream, model_cls_callback, model_callback)
                task = loop.create_task(coro)
                # ensure the thread stays open until processing is complete.
                # generally, this should run until the stream is closed
                cofuture = cofutures.Future
                task.add_done_callback(lambda _: cofuture.set_result(True))
                _ = cofuture.result()

            chunk: Optional[bytes] = yield  # type: ignore
            if not chunk:
                ## effective EOF
                await stream.aclose()
                raise NoResponse(response_info.status, response_info.reason)

            ## feed the response to the chunk stream
            ##
            ## for conventional REST endpoints with the v20 fxTrade servers,
            ## this would typically represent the entire response body
            await stream.feed(chunk)

            ## assumption: The caller will have provided a model_callback that will handle
            ## any response object(s) in a manner suitable for the request
            await controller.dispatch(parse_response)

            while chunk:
                chunk = yield True  # type: ignore
                stream.feed(chunk)
            await stream.aclose()
            return


class SequenceBuilder(InstanceBuilder[Sequence]):

    __slots__ = tuple(set(InstanceBuilder.__slots__).union({"transport_type"}))

    def __init__(self, transport_type: TransportValues, origin: ModelBuilder):
        super().__init__(list, origin)
        ## transport_type may be none when parsing a mapping under an unralized abstract type
        self.transport_type = transport_type

    def instance_prototype(self) -> Sequence:
        return []

    async def aevent(self, event: str, value: Any):  # type: ignore
        builder = self.builder
        if builder is self:
            if __debug__:
                model_builder_debug("SequenceBuilder.aevent %s %s (%s)", self.key, event, self.instance_class.__name__ if self.instance_class else None)
            match event:
                case 'start_array':
                    self.instance = []
                    return
                case 'end_array':
                    self.finalized = True
                case 'map_key':
                    raise ValueError("map_key not supported in SequenceBuilder", self)
                case 'start_map':
                    member_type_class: Optional[ApiClass]
                    if self.transport_type:
                        member_type_class = self.transport_type.member_transport_type.storage_class
                    else:
                        ## parsing a mapping under an unrealized abstract type
                        member_type_class = None
                    builder = ModelBuilder(member_type_class, self)
                    self.builder = builder
                    await builder.aevent(event, value)
                case _:
                    parsed = None
                    if self.transport_type:
                        parsed = self.transport_type.parse_member(value)
                    else:
                        # defer deserialization when parsing under an unrealized abstract type
                        parsed = value
                    self.instance.append(parsed)  # type: ignore
        else:
            await builder.aevent(event, value)
            if builder.builder is builder:
                match event:
                    case 'end_map' | 'end_array':
                        if builder.finalized:
                            self.instance.append(builder.instance)  # type: ignore
                            del builder
                            self.builder = self
