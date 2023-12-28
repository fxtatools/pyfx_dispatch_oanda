# origianlly tokenize-ijson.py - tokenization tests for an application of ijson

from abc import abstractmethod, ABC
import asyncio as aio
from contextlib import closing
import ijson  # type: ignore[import-untyped]
import logging
import os
import sys
import time

from typing import Any, Generic, Mapping, Optional, Sequence, Union, TYPE_CHECKING
from typing_extensions import Generic, Self, TypeVar

from .io import AsyncSegmentChannel, DataError
from .transport import (   # type: ignore
    ApiObject, AbstractApiObject, InterfaceClass,
    TransportFieldInfo, TransportType, TransportInterface, TransportValuesType
)


class NoResponse(DataError):
    pass

##
## The builder model for applying ijson with the ApiObject model
##


T = TypeVar("T")
Tmodel = TypeVar("Tmodel", bound=InterfaceClass)

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

    builder: Union["InstanceBuilder", Self]
    '''The next builder for event forwarding, or this instance itself'''

    finalized: bool
    '''Flag for indicating whether the builder has reached end-of-object in the input stream'''

    def finalize_builder(self):
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
    __slots__ = tuple(set(InstanceBuilder.__slots__).union({"json_fields", "designator_key", "realize_abstract"}))

    json_fields: Mapping[str, TransportFieldInfo]
    """
    Mapping of field names and field alias names to field information objects
    for the instance class.
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

    if TYPE_CHECKING:
        instance_class: Union[AbstractApiObject, ApiObject]

    def __init__(self, cls: Optional[type[ApiObject]], origin: Optional[InstanceBuilder] = None):
        ## the model class `cls` should be provided at a top level. The value may be None
        ## when parsing a mapping under an unrealized abstract type
        self.realize_abstract = False
        if __debug__:
            if cls and not isinstance(cls, type):
              raise AssertionError("Not a type", cls)
        if cls and issubclass(cls, AbstractApiObject):
            self.designator_key = cls.designator_key
        else:
            self.designator_key = None
        super().__init__(cls, origin)
        self.json_fields = cls.json_fields if cls else None

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
        # json_fields may be None when parsing for an unrealized abstract type
        fields = self.json_fields
        if fields and key in fields:
            return fields[key].name
        elif isinstance(self.instance, Mapping):
            # parsing an abstract type
            return key
        else:
            raise ValueError("Unknown JSON field name", key, self.instance_class)

    def get_field_transport_type(self, key: str) -> Optional[TransportType]:
        ## may return None, e.g during 'start_map' under an unrealized abstract type
        if not self.instance_class or issubclass(self.instance_class, AbstractApiObject):
            return None
        json_fields = self.json_fields
        if key in json_fields:
            field = json_fields[key]
            if isinstance(field, TransportFieldInfo):
                ttyp = field.transport_type
                assert ttyp, "Field has a null transport type"
                return ttyp
            else:
                raise RuntimeError("Parser transport type inferrence is not supported")
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
                assert self.instance_class, "Null instance class"
                ttyp = self.instance_class.get_transport_type(annot) ## ?
                if ttyp:
                    return ttyp
                else:
                    raise ValueError("No transport type found", key, annot, self.instance_class)
        else:
            raise ValueError("Unknown JSON field", key, self.instance_class, set(json_fields.keys()), self.instance)

    def set_field(self, value: Any):
        key: str = self.key  # type: ignore
        if isinstance(self.instance, ApiObject):
            # when not deferring initialization with a dict mapping,
            # ensure field tracking for applications onto Pydantic
            attr_key = self.json_fields[key].name
            self.instance.model_fields_set.add(attr_key)
            ## setattr via ApiObject and pydantic methods, also ensuring
            ## value translation during init, e.g str => enum
            return setattr(self.instance, attr_key, value)
        else:
            # assumption: self.instance is a dictionary, or a dict-like  object
            # such that can be accessed with a string subscript
            self.instance[key] = value  # type: ignore
        self.key = None

    def realize_instance(self, type):
        # utility method for application when parsing an abstract API object type
        inst = self.instance_class.realize_map(type, self.instance)
        concrete_cls: Tmodel = inst.__class__
        self.instance_class = concrete_cls
        self.json_fields = concrete_cls.json_fields
        self.instance = inst
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
            if event == "start_map":
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
            elif event == 'end_map':
                # Implementation Note:
                # Using one model builder per top-level element,
                # streaming or otherwise in the reader protocol
                if __debug__:
                    model_builder_debug("Finalizing %r", self.instance)
                self.finalize_builder()
                if async_callback:
                    if __debug__:
                        model_builder_debug("Dispatch to callback for %r", self.instance)
                    await async_callback(self.instance)
                return
            elif event == 'map_key':
                # try:
                self.key = value
                # except ValueError as exc: ## previously ...
                #     if value == self.designator_key:
                #         # Assumption: the next parser event should provide
                #         # the value for the designator key
                #         self.realize_abstract = True
                #         self.key = value
                #     else:
                #         raise
            elif event == 'start_array':
                # create a new sequence builder for event forwarding
                #
                # this assumes that the containing field is decribed with
                # a values-typed field info instance, such that the internal
                # member class for the field is represented in the provided
                # field info
                inst_cls: Tmodel = self.instance_class
                ## field may be null when parsing a mapping under an unrealized abstract type
                field: TransportFieldInfo = inst_cls.json_fields.get(self.key, None) if inst_cls else None  # type: ignore
                member_transport: TransportValuesType = field.transport_type if field else None
                builder = SequenceBuilder(member_transport, self)
                self.builder = builder
                await builder.aevent(event, value)
            elif event == 'end_array':
                seq = builder.instance
                self.set_field(tuple(seq))
                self.builder = self
            elif event == 'string':
                # if self.realize_abstract:
                #     self.realize_instance(value)
                if self.designator_key is not None and self.key == self.designator_key:
                    ## FIXME TEST UPDATE && remove the realize_abstract field
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
                    if __debug__:
                            ## state flag for backtrace
                        parse_deferred = True
                    parsed = value
                else:
                    if __debug__:
                        if not (issubclass(transport, TransportInterface) or isinstance(transport, TransportInterface)):
                            raise AssertionError("Not a transport type", transport)
                    parsed = transport.parse(value)
                    if __debug__:
                            ## state flag for backtrace
                        parse_deferred = False
                self.set_field(parsed)
            else:
                self.set_field(value)
        else:
            # dispatch to the forwarded builder
            await builder.aevent(event, value)
            if builder.builder is builder:
                # process the builder for finalization
                if event == 'end_map' or event == 'end_array':
                    if builder.finalized:
                        # set the last parsed key value to the
                        # newly initialized object
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
    def from_text(cls, model_cls: type[Tmodel], data: Union[bytes, str],
                  loop: Optional[aio.AbstractEventLoop] = None) -> Tmodel:
        ## generic synchronous interface for the async JSON parser
        ## used only under tests, locally ... such as under ApiObject.from_json()
        coro = cls.from_text_async(model_cls, data)
        if loop:
            if loop.is_running():
                task = loop.create_task(coro)
                delay = sys.getswitchinterval()
                while not task.done():
                    time.sleep(delay)
                return task.result()
            else:
                loop.run_until_complete(coro)
        else:
            policy = aio.get_event_loop_policy()
            ctx_loop = policy.get_event_loop()
            if ctx_loop.is_closed():
                with closing(policy.new_event_loop()) as new_loop:
                    ret = new_loop.run_until_complete(coro)
                    new_loop.stop()
                    return ret
            else:
                return ctx_loop.run_until_complete(coro)


class SequenceBuilder(InstanceBuilder[Sequence]):

    __slots__ = tuple(set(InstanceBuilder.__slots__).union({"transport_type"}))

    def __init__(self, transport_type: TransportValuesType, origin: ModelBuilder):
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
            if event == 'start_array':
                self.instance = []
                return
            elif event == 'end_array':
                self.finalized = True
            elif event == 'map_key':
                raise ValueError("map_key not supported in SequenceBuilder", self)
            elif event == 'start_map':
                member_type_class: Optional[type[ApiObject]]
                if self.transport_type:
                    member_type_class = self.transport_type.member_transport_type.storage_class
                else:
                    ## parsing a mapping under an unrealized abstract type
                    member_type_class = None
                builder = ModelBuilder(member_type_class, self)
                self.builder = builder
                await builder.aevent(event, value)
            else:
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
                if event == 'end_map' or event == 'end_array':
                    if builder.finalized:
                        # add the completed instance
                        self.instance.append(builder.instance)  # type: ignore
                        del builder
                        self.builder = self
