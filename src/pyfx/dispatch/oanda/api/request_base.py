## requests.py

##
## Request Class Prototypes
##

import concurrent.futures as cofutures
from abc import abstractmethod, ABC
import asyncio as aio
from collections import ChainMap
from collections.abc import Generator, Mapping
from contextlib import asynccontextmanager, contextmanager, suppress
from functools import partial
import httpcore
import httpx
import inspect
import ijson  # type: ignore[import-untyped]
import reprlib
from immutables import Map
import logging
from pydantic import field_validator
from queue import SimpleQueue, Empty
import re
import sys
from typing import Annotated, Any, AsyncIterator, Awaitable, Callable, ContextManager, Generic, Iterator, Literal, Mapping, Optional, Self, Union, TYPE_CHECKING
from typing_extensions import ClassVar, TypeAlias, TypeVar


# from pydantic.config import ConfigDict

from ..finalizable import Finalizable
from ..util.singular_map import SingularMap
from ..util.aio import safe_running_loop, chain_cancel_callback, cancel_when_done
from ..util.log import configure_logger
from ..util.cofuture import CoFuture

from ..configuration import FxHostInfo

from ..api.transport_client import TransportClient
from ..exceptions import ApiException
from ..response_common import REST_CONTENT_TYPE
from ..parser import ModelBuilder
from ..io.segment import AsyncSegmentChannel, DataError

from ..models.response_mixins import ApiResponse, ApiErrorResponse, UnknownErrorResponse

from ..exec_controller import ExecController, thread_loop
from ..request_constants import RequestMethod

from ..transport.transport_base import TransportFieldInfo
from ..transport.data import InterfaceClass, InterfaceModel, AbstractApiObject, ApiObject
from ..transport.application_fields import ApplicationField

from .param_info import ParamInfo, PathParamInfo, QueryParamInfo, path_param


logger = logging.getLogger(__name__)


def set_future_exception(future: aio.Future, exception: Exception) -> Optional[aio.Handle]:
    """Set the exception for a future, in a thread-safe approach.

    If the future's loop is the running loop, the exception will
    be set directly to the future.

    If the future's loop is not the running loop, the exception will
    be set as with `loop.call_soon_threadsafe(...)` using the future's
    loop.
    """
    if not future.done():
        if isinstance(future, CoFuture):
            future.set_exception(exception)
            return
        loop: aio.AbstractEventLoop = future.get_loop()
        running = safe_running_loop()
        if running is loop:
            with suppress(aio.InvalidStateError, aio.CancelledError):
                future.set_exception(exception)
        else:
            return loop.call_soon_threadsafe(future.set_exception, exception)


def set_future_result(future: aio.Future, result: Any) -> Optional[aio.Handle]:
    """Set the result for a future, in a thread-safe approach.

    If the future's loop is the running loop, the result will
    be set directly to the future.

    If the future's loop is not the running loop, the result will
    be set as with `loop.call_soon_threadsafe(...)` using the future's
    loop.
    """
    if not future.done():
        if isinstance(future, CoFuture):
            future.set_result(result)
            return
        loop = future.get_loop()
        if aio.get_running_loop() is loop:
            with suppress(aio.InvalidStateError, aio.CancelledError):
                future.set_result(result)
        else:
            return loop.call_soon_threadsafe(future.set_result, result)


@contextmanager
def safe_await():
    ## useless in fact

    #with suppress(aio.CancelledError, RuntimeError):
    with suppress(aio.CancelledError):
        # RuntimeError may occur here, during controller shutdown
        yield

#
# Controller Base
#

T_co = TypeVar("T_co", covariant=True)

T_request_co = TypeVar("T_request_co", covariant=True, bound="ApiRequest")

T_response = TypeVar("T_response", bound=ApiResponse)
T_value = TypeVar("T_value", bound=ApiResponse)

Response_contra = TypeVar("Response_contra", bound=ApiResponse, contravariant=True)


class RequestController(ExecController):
    ## Stateless request controller class for the v20 API

    __slots__ = tuple(list(ExecController.__slots__) + ["rest_client"])

    rest_client: TransportClient

    @classmethod
    def configure_loggers(cls):
        super().configure_loggers()
        handlers = logging.getLogger().handlers
        configure_logger("hpack", handlers=handlers,
                         level=logging.WARNING)

    def initialize_defaults(self):
        super().initialize_defaults()
        if not hasattr(self, "rest_client"):
            self.rest_client = TransportClient(self)

    class RequestBuilder(Finalizable, Generic[T_request_co]):
        __slots__ = "request_class", "request_args"

        request_class: type[T_request_co]
        request_args: Union[dict[str, Any], Map[str, Any]]

        if TYPE_CHECKING:
            ## type hints for common request arg <=> builder attr values
            controller: "RequestController"
            ## A Response Future should generally not be initialized
            ## within a request builder scope. The future should be
            ## initialized uniquely, to each individual Request object
            # future: aio.Future[Response_contra]

        def __init__(self, request_class: type[T_request_co], **request_kw):
            self.request_class = request_class
            self.request_args = request_kw

        def __finalize_instance__(self):
            if not self.__finalized__:
                self.request_args = Map(self.request_args)
                super().__finalize_instance__()

        def __iter__(self):
            return self.request_args.__iter__()

        def override_args(self, args: Mapping[str, Any]) -> Mapping[str, Any]:
            if len(args) == 0:
                return self.request_args
            elif self.__finalized__:
                with self.request_args.mutate() as derived:
                    for name, val in args.items():
                        derived[name] = val
                    return derived.finish()
            else:
                return ChainMap(args, self.request_args)

        def mutate(self, **args) -> Self:
            new_args = self.override_args(args)
            return self.__class__(self.request_class, **new_args)

        def build(self, **kw) -> tuple[T_request_co, aio.Future[Response_contra]]:
            if not ("future" in kw or "future" in self.request_args):
                kw["future"] = self.controller.add_cofuture(self.request_class.request_path)
            args = self.override_args(kw)
            future = args["future"]
            return self.request_class(**args), future

        def add_args(self, **args: Mapping[str, Any]):
            if self.__finalized__:
                raise ValueError("Builder is finalized", self)
            rcls = self.request_class
            fields = rcls.model_fields
            for name, value in args.items():
                if name in fields:
                    arg_value = value
                    info = fields[name]
                    if isinstance(info, TransportFieldInfo):
                        txtyp = info.transport_type
                        if not isinstance(value, txtyp.storage_class):
                            arg_value = txtyp.parse(value)
                    self.request_args[name] = arg_value
                else:
                    raise ValueError("Unknown request field", name, rcls)

        def __getattr__(self, name: str) -> Any:
            args = self.request_args
            if name in args:
                return args[name]
            else:
                raise AttributeError("Not a bound arg", name)

    @contextmanager
    def request_builder(self,
                        request_cls: type[T_request_co]
                        ) -> Generator[RequestBuilder[T_request_co], None, None]:
        builder = self.RequestBuilder[T_request_co](
            request_cls,
            controller=self,
            host=self.config.get_host(),
            account_id=self.config.account_id
        )
        yield builder
        ## finalize the builder
        builder.__finalize_instance__()

    @contextmanager
    def run_context(self) -> Iterator[Self]:
        ApiObject.types_repository.__finalize_instance__()
        with super().run_context() as supra:
            yield supra

    @asynccontextmanager
    async def async_context(self) -> AsyncIterator[aio.TaskGroup]:
        async with super().async_context() as tg:
            async with self.rest_client:
                yield tg
            if __debug__:
                logger.debug("exiting async context")
        if __debug__:
            logger.debug("exited task group")


#
# Request Classes
#


PathTokens: TypeAlias = tuple[Union[bytes, ParamInfo]]


class ApiRequestClass(InterfaceClass, type):
    """Metaclass for ApiRequest definitions"""

    request_method: RequestMethod
    """The HTTP request method"""

    request_path: str
    """Parameterized path for the request

    This value should be provided as an absolute URL path,
    such that may be appended to the host path for a request.

    For v20 API requests, this string should not include
    the path component '/v3', such that would provided in
    the host path.
    """
    path_tokens: PathTokens

    path_params: Optional[Map[str, ParamInfo]]
    """Parameters for the request path, if applicable.

    When defined as a Mapping object, each parameter in
    the mapping denotes a required parameter for the
    request class.

    When defined as the value None, the request will not
    accept path parameters.
    """

    query_params: Optional[Map[str, ParamInfo]]
    """Query parameters for the request, if applicable."""

    response_types: Map[int, type[ApiObject]]
    """Mapping of response type codes to expected response types.

    This mapping is derived from the original v20 JSON API description.

    For a server response code not in this mapping or a response provied
    with a response code outside of the range `[200, 299]` (inclusive),
    the response would generally be qualified as a server error response
    and raised with an exception during response processing.

    This mapping will generally define at most once response code
    within the range `[200, 299]` (inclusive). The corresponding response
    type will be defined under the `primary_type` attribute for the
    request class.  The server response code for this type will  be defined
    as the `primary_status` for the request class.
    """

    primary_status: ClassVar[int]
    """Primary status code for a successful server response under the
    request class.

    If this value is not set within the definition of the request class,
    then the value will be inferred from the contents of the request class'
    `response_types` mapping.
    """

    primary_type: type[ApiObject]
    """Primary response object type for a successful server response under
    the request class.

    If this value is not set within the definition of the request class,
    then the value will be inferred from the contents of the requests class'
    `response_types` mapping.
    """

    def __repr__(cls):
        unbound = "<unbound>"
        mtd = cls.request_method if hasattr(cls, "request_method") else unbound
        path = cls.request_path if hasattr(cls, "request_path") else unbound
        return "<%s %s %s>" % (cls.__name__, mtd, path)

    def simplify_param_model(cls, model: Mapping[str, ParamInfo]) -> Optional[Mapping[str, ParamInfo]]:
        """Reduce a parameters model to None, a SingularMap, or an immutable Map.

        If the parameters model `model` contains no mapped values, returns `None`

        If the model contains one mapped value, returns a new SingularMap.

        Else, returns an immutable Map for the provided paratemters model.
        """
        if not model:
            return None
        n_mapped = len(model)
        if n_mapped is int(0):
            return None
        elif n_mapped is int(1):
            for name, info in model.items():
                return SingularMap(name, info)
        else:
            return Map(model)

    def init_field_info(self, field_name: str, info: TransportFieldInfo):
        """Initialize a ParamInfo object for the request class"""
        super().init_field_info(field_name, info)
        if isinstance(info, PathParamInfo):
            path_params = self.path_params
            if __debug__:
                if path_params is None:
                    raise AssertionError("Received PathParamInfo for a class with no path_params", info, self)
            if field_name not in path_params:
                path_params[field_name] = info
        elif isinstance(info, QueryParamInfo):
            query_params = self.query_params
            if __debug__:
                if query_params is None:
                    raise AssertionError("Received QueryParamInfo for a class with no query_params", info, self)
            if field_name not in query_params:
                query_params[field_name] = info
        # elif __debug__:
        #     raise AssertionError("Unmanaged request model field", field_name, info)

    def __new__(mcls: type[Self], name: str,
                bases: tuple[type, ...],
                attrs: dict[str, Any],
                **kw) -> Self:
        """Initialize a new request class"""

        if "path_params" not in attrs:
            attrs["path_params"] = dict()
        if "query_params" not in attrs:
            attrs["query_params"] = dict()
        if "response_types" in attrs:
            # inference for primary response status and type,
            # when not provided in the class definition
            response_types: Mapping[int, type[ApiObject]] = attrs["response_types"]
            primary_status = None
            primary_type = None
            if len(response_types) == 1:
                for status, t in response_types.items():
                    primary_status = status
                    primary_type = t
                    break
            else:
                success_codes = []
                for status in response_types.keys():
                    if 200 <= status <= 299:
                        ## typically the default response code,
                        ## not always 200
                        success_codes.append(status)
                if len(success_codes) == 1:
                    primary_status = success_codes[0]
                    primary_type = response_types[primary_status]
            if primary_status and "primary_status" not in attrs:
                attrs["primary_status"] = primary_status
            if primary_type and "primary_type" not in attrs:
                attrs["primary_type"] = primary_type

        new_cls: Self = super().__new__(mcls, name, bases, attrs, **kw)

        if not hasattr(new_cls, "request_method"):
            new_cls.request_method = RequestMethod.GET

        new_cls.path_params = new_cls.simplify_param_model(new_cls.path_params)
        new_cls.query_params = new_cls.simplify_param_model(new_cls.query_params)

        if hasattr(new_cls, "request_path") and not hasattr(new_cls, "path_tokens"):
            new_cls.path_tokens = new_cls.tokenize_path(new_cls.request_path)

        return new_cls


class ApiRequest(InterfaceModel, ABC, Generic[T_response, T_value], metaclass=ApiRequestClass):

    #
    # Common ApiRequest class variables
    #

    request_path: ClassVar[str]
    """Metaclass instance attribute, described in {py:obj}`ApiRequestClass.request_path`"""

    request_method: ClassVar[RequestMethod]
    """Metaclass instance attribute, described in {py:obj}`ApiRequestClass.request_method`"""

    path_tokens: ClassVar[PathTokens]
    """Metaclass instance attribute, described in {py:obj}`ApiRequestClass.path_tokens`"""

    path_params: ClassVar[Optional[Map[str, PathParamInfo]]]
    """Metaclass instance attribute, described in {py:obj}`ApiRequestClass.path_params`"""

    query_params: ClassVar[Optional[Map[str, QueryParamInfo]]]
    """Metaclass instance attribute, described in {py:obj}`ApiRequestClass.query_params`"""

    primary_status: ClassVar[int]
    """Metaclass instance attribute, described in {py:obj}`ApiRequestClass.primary_status`"""

    primary_type: ClassVar[type[ApiObject]]
    """Metaclass instance attribute, described in {py:obj}`ApiRequestClass.primary_type`"""

    response_types: ClassVar[Map[int, type[ApiObject]]]
    """Metaclass instance attribute, described in {py:obj}`ApiRequestClass.response_types`"""

    #
    # Common ApiRequest instance fields
    #

    # future: Annotated[aio.Future[T_response], ApplicationField(..., default_factory=aio.Future)]
    ## nuts !
    future: Annotated[Union[CoFuture[T_response], aio.Future[T_response]], ApplicationField(..., default_factory=CoFuture)]
    """Response future for the API request"""

    controller: Annotated[RequestController, ApplicationField(...)]
    """Request controller for the API request"""

    host: Annotated[FxHostInfo, path_param(...)]
    """Destination host definition for the API request

    In application for v20 API requests, the FxHostInfo value represents a generalization of
    REST and Streaming endpoint hosts. The actual hostname will determined for the request
    endpoint, when the request is dispatched.

    For v20 API requests, streaming requests will use a different host than general REST
    requests. Sach set of REST and Streaming hosts will differ respectively for fxPractice
    and fxLive accounts.

    This value would generally be inferred by a request bulder, using the configuration for
    the request controller. If the configuration is for a demo i.e practice account
    (the default), this value should be `FxHostInfo.fxPractice`. For live account
    requests, `FxHostInfo.fxLive`
    """

    @field_validator("controller", check_fields=False, mode="plain")
    @classmethod
    def validate_controller(cls, controller):
        """Interoperability for parameter validation in Pydantic 2"""
        if isinstance(controller, RequestController):
            return controller
        else:
            raise ValueError("Unknown controller", controller)

    def __repr__(self):
        cls = self.__class__
        unbound = "<unbound>"
        mtd = cls.request_method if hasattr(cls, "request_method") else unbound
        path = cls.request_path if hasattr(cls, "request_path") else unbound
        host = str(self.host) if hasattr(self, "host") else unbound
        ftr = str(self.future) if hasattr(self, "future") else unbound
        return "<%s %s %s %s (%s) at 0x%x>" % (cls.__name__, mtd, path, host, reprlib.repr(ftr), id(self))

    @classmethod
    def ensure_transport_type(self) -> None:
        pass

    @classmethod
    def tokenize_path(cls, path: str) -> Iterator[Union[str, ParamInfo]]:
        """Tokenize a request path, returning a sequcence of parameter info
        and contiguous string values"""
        if __debug__:
            if not isinstance(path, str):
                raise AssertionError("Not a string", path)
        param_info = cls.path_params
        json_param_info = dict({info.alias or field_name: info for field_name, info in param_info.items()})
        parsed_start: bool = False
        text: Optional[str] = None
        for token in path.split("/"):
            if len(token) == 0:
                if parsed_start:
                    raise AssertionError("Empty token in request path", path)
                else:
                    parsed_start = True
            elif token[0] == "{":
                if __debug__:
                    if token[-1] != "}" or len(token) < 3:
                        raise AssertionError("Syntax error in request path", path)
                if text:
                    yield text
                    text = None
                param_name = token[1:-1]
                if __debug__:
                    if not (param_name in json_param_info):
                        raise AssertionError("Path parameter not defined in param info", param_name, param_info, cls)
                yield json_param_info[param_name]
            else:
                if text:
                    text = text + '/' + token
                else:
                    text = token
        ## yield any trailing path
        if text:
            yield text

    @classmethod
    def process_param_str(self, param: Union[bytes, ParamInfo], values: Mapping[str, Any]) -> str:
        """process a path parameter to a URL string, given field values for a request,
        or return param if param is a URL string component

        values: generally produced from `path_values()`

        param: a string value or a path parameter, as via `fill_path_str()``
        """
        if isinstance(param, str):
            ## literal param token
            return param
        else:
            if __debug__:
                if not isinstance(param, ParamInfo):
                    raise AssertionError("Parameter token is not str or a ParamInfo object", param)
            name = param.json_name
            if __debug__:
                if name not in values:
                    raise AssertionError("No value provided for parameter", name, param, values)
            value = values[name]
            return param.transport_type.unparse_url_str(value)

    @classmethod
    def fill_path_str(self, values) -> bytes:
        """process the request class' tokenized URL path to a string

        this string will not include any generally optional query segment
        """
        return "/".join(self.process_param_str(token, values) for token in self.path_tokens)

    @classmethod
    def path_values(cls, instance: Self) -> Optional[Mapping[str, Any]]:
        """return a mapping of path parameter names to instance field values, if the instance
        is defined with path parameters, else None.

        Each key in the mapping will represent a JSON parameter name. Each value will
        represent a value from a bound field of the instance.
        """
        params = cls.path_params
        if params:
            path_param_names = instance.model_fields_set.intersection(frozenset(params.keys()))
            if path_param_names:
                return {params[name].json_name: getattr(instance, name) for name in path_param_names}

    @classmethod
    def query_values(cls, instance: Self) -> Optional[Mapping[str, Any]]:
        """return a mapping for query parameters bound within a request instance

        Each key in the mapping will represent an internal field name from the
        set of query parameters for the request class, `cls`. Each value will
        represent a field value expressly bound in the request `instance`.

        This function may applied as a filter for values to be provided to
        {py:obj}`fill_query_str()`
        """
        params = cls.query_params
        if params:
            query_param_names = instance.model_fields_set.intersection(set(params.keys()))
            if query_param_names:
                return {name: getattr(instance, name) for name in query_param_names}

    @classmethod
    def fill_query_str(cls, values: Optional[Mapping[str, Any]] = None) -> Optional[str]:
        """Return any query string for a request, provided with a mapping for request
        parameter values.

        Returns None if `values` does not provide any query parameters for the request
        clss.

        ### Implementation Notes

        This method has been implemented as, in effect, a direct transformatiom from
        internal field names and values in a `values` mapping to a URL query string
        using JSON parameter names.

        The `values` mapping may be produced generally with {py:obj}`query_values()`
        such as to limit the `values` mapping to the set of query parameter fields
        bound within a request instance.

        Additional caveats, for this implementation:

        - The return value will be either `None` or a contiguous string. If a string,
          the value will represent a URL-encoded string, not including the query
          prefix `"?"`. The value `None` would indicate that the `values` did not
          include any query components for the request class.

        - This method will return None if the class does not define any query
          parameters
        """
        if values:
            query_fields: Optional[Mapping[str, TransportFieldInfo]] = cls.query_params
            if query_fields:
                return "&".join(
                    query_fields[name].json_name + "=" + query_fields[name].transport_type.unparse_url_str(value)
                    for name, value in values.items()
                )

    #
    # ApiRequest => response dispatch
    #

    # @classmethod
    # def initialize_builder(cls, builder: RequestController.RequestBuilder[Self]):
    #     pass

    @classmethod
    @contextmanager
    def request_builder(cls, controller: RequestController, **kw
                        ) -> ContextManager[RequestController.RequestBuilder[Self]]:
        with controller.request_builder(cls, **kw) as builder:
            yield builder

    @classmethod
    def build_request(cls, controller: RequestController, **kw
                      ) -> RequestController.RequestBuilder[Self]:
        with cls.request_builder(controller, **kw) as builder:
            return builder

    def activate_callback(self, future: aio.Future) -> Awaitable[Optional[aio.Task[aio.Future[T_response]]]]:
        cancelled = False
        with suppress(aio.InvalidStateError, aio.CancelledError):
            if future.cancelled() or future.exception():
                cancelled = True
                self.future.cancel()
        if cancelled:
            return
        else:
            return self.controller.add_task(self.dispatch_request())

    @classmethod
    def f_builder(cls,
                  builder: RequestController.RequestBuilder[Response_contra]
                  ) -> tuple[aio.Future[Response_contra], RequestController.RequestBuilder[Response_contra]]:
        if "future" in builder:
            return builder["future"], builder
        else:
            future = builder.controller.add_cofuture()
            bld = builder.mutate(future=future)
            return future, bld

    def callback_coro_success(self,
                              callback: Callable[[T_response], Awaitable[T_co]],
                              future: aio.Future[T_response]) -> Optional[aio.Task[T_co]]:
        # utility function for add_success_callback, given a callback provided as a coroutine function
        if not (future.cancelled() or future.exception()):
            return self.controller.add_task(callback(future.result()))

    def callback_func_success(self,
                              callback: Callable[[T_response], Any],
                              future: aio.Future[T_response]) -> Optional[aio.Handle]:
        # utility function for add_success_callback, given a callback provided as a non-coroutine function
        if not (future.cancelled() or future.exception()):
            return self.controller.main_loop.call_soon(callback, future.result())

    def add_success_callback(self, callback: Callable[[T_response], Any]):
        if inspect.iscoroutinefunction(callback):
            func = partial(self.callback_coro_success, callback)
        else:
            func = partial(self.callback_func_success, callback)
        self.future.add_done_callback(func)

    @classmethod
    def activate_from(cls,
                      # future: aio.Future[Response_contra],
                      # builder: RequestController.RequestBuilder[Self],
                      builder: RequestController.RequestBuilder[Response_contra],
                      cb: Optional[Callable[[Response_contra], Mapping[str, Any]]] = None
                      ) -> tuple[aio.Future[T_response], Callable[[aio.Future[Response_contra]], Any]]:

        future, bld = cls.f_builder(builder)

        def proto_cb(req_ftr: aio.Future[Self],
                     bld: RequestController.RequestBuilder[Self],
                     cb: Optional[Callable[[Response_contra], Mapping[str, Any]]],
                     response_ftr: aio.Future[Response_contra]):
            if response_ftr.cancelled() or response_ftr.exception() or req_ftr.done():
                return
            try:
                controller: RequestController = bld.controller
                result = response_ftr.result()
                args = None if cb is None else cb(result)
                req, _ = bld.build(**args) if args else bld.build()
                controller.add_task(req.dispatch_request())
            except Exception as e:
                with suppress(aio.InvalidStateError):
                    set_future_exception(req_ftr, e)
                raise

        partial_cb = partial(proto_cb, future, bld, cb)
        future.add_done_callback(partial_cb)
        return future, partial_cb

    def activate_from_cb(self, future: aio.Future):
        future.add_done_callback(self.activate_callback)

    async def aeach_object(self, timeout: Union[int, float] = 0) -> AsyncIterator[T_value]:
        raise NotImplementedError(self.aeach_object)

    async def get_response_type(self, client_response: httpx.Response,
                                stream: AsyncSegmentChannel[bytes]) -> Optional[Union[type[ApiObject], Literal[False]]]:
        status = client_response.status_code
        if status == self.primary_status:
            return self.primary_type
        else:
            ## None: Typically a server error response,
            ## response object type can be inferred externally
            ## Type: May represent a server error response
            ## having some specific response object type.
            ##
            ## "Error" interpretation of the response depends
            ## generally on the response status code
            return self.__class__.response_types.get(status, None)

    async def dispatch_response(self,
                                response: Union[ApiObject, Literal[False]],
                                client_response: httpx.Response,
                                initial_request: httpx.Request):
        status = client_response.status_code
        ## False: Response processing was skipped
        if status and 200 <= status <= 299:
            self.put_response(response)
        else:
            ## set an exception indicating the server error response
            reason = client_response.reason_phrase
            api_exc = ApiException(status=status, reason=reason, response=response)
            self.put_error_response(api_exc)

    def put_response(self, response: T_response) -> Optional[aio.Handle]:
        # utility method for response processing
        with suppress(aio.InvalidStateError, aio.CancelledError):
            return set_future_result(self.future, response)

    def put_error_response(self, error: ApiException) -> Optional[aio.Handle]:
        # utility method for response processing
        with suppress(aio.InvalidStateError, aio.CancelledError):
            set_future_exception(self.future, error)

    def request_host(self) -> str:
        return self.host.rest_host

    async def prepare_request(self) -> httpx.Request:

        cls = self.__class__
        path_values = cls.path_values(self)

        if __debug__:
            logger.info("Processing REST request %s %s", cls.request_method, cls.request_path)

        path_str = self.request_host() + '/' + cls.fill_path_str(path_values)

        query_str = cls.fill_query_str(cls.query_values(self))
        if query_str:
            path_str = path_str + '?' + query_str

        request_method = bytes(cls.request_method)

        return self.controller.rest_client.client.build_request(request_method, path_str)

    # @asynccontextmanager
    # async def rest_request(self) -> aio.Future[T_response]:
    #     async with self.prepare_request().stream() as client_response:
    #         ## ^ looses the request object ...
    #         yield client_response

    # def create_synchronous_client(self, request: httpx.Request):
    #     return httpx.Client(self.controller.rest_client.client....)

    @asynccontextmanager
    async def request_stream(self, request: httpx.Request):
        response_future = self.future
        controller = self.controller
        if response_future.done():
            logger.critical("response future is closed: %r, %r", response_future, self)
            return
        client = controller.rest_client.client
        main = controller.main_loop
        th_loop = aio.get_running_loop()
        coro = client.send(request, stream=True)
        if client.is_closed:
            raise RuntimeError("Client is closed", client, self)
        elif th_loop is main:
            client_response = await coro
        else:
            # here, the request is probably initialized under a worker thread.
            cf = aio.run_coroutine_threadsafe(coro, main)
            chain_cancel_callback(response_future, cf)
            interval = sys.getswitchinterval()
            while not cf.done():
                await aio.sleep(interval)
            client_response = cf.result()
        try:
            yield client_response
        finally:
            with suppress(cofutures.CancelledError, aio.CancelledError):
                await self.future
            ## ! closing the client response here, as a fallback
            with suppress(aio.CancelledError):
                await client_response.aclose()

    async def dispatch_request(self) -> Awaitable[aio.Future[T_response]]:
        request = await self.prepare_request()
        response_future = self.future
        async with self.request_stream(request) as client_response:
            proc_coro = self.process_response(client_response, request)
            proc_task: aio.Task = self.controller.add_task(proc_coro)
            chain_cancel_callback(response_future, proc_task)
            chain_cancel_callback(proc_task, response_future)
            if __debug__:
                ## note for logging/serialization: response_headers.get("requestid")
                logger.info("request: Processing response: %r", self)
            with suppress(aio.CancelledError):
                await proc_task
        return response_future

    async def process_response(self, client_response: httpx.Response, initial_request: httpx.Request):
        if __debug__:
            if not isinstance(client_response, httpx.Response):
                raise AssertionError("not an httpx response]", client_response)
        try:
            response_future = self.future

            async with AsyncSegmentChannel[bytes]() as stream:
                # stream.closed_future.add_done_callback(lambda _: print("---- Stream is closed: %r" % repr(self)))
                response_future.add_done_callback(lambda _: stream.close())

                if __debug__:
                    logger.debug("process_response: dispatch to parse_response thread")

                thr_future = self.controller.dispatch(
                    self.parse_response, stream, client_response, initial_request
                )
                cancel_when_done(response_future, thr_future)

                try:
                    async for chunk in client_response.aiter_bytes():
                        if response_future.done():
                            return
                        await stream.feed(chunk)
                except Exception as exc:
                    ## break on short read, e.g when closing a streaming request
                    pass

                ## feed EOF and close the client_response
                if not stream.closed():
                    with suppress(DataError):
                        await stream.feed(b'', True)
                await client_response.aclose()

                ## keep the context manager and this end of the stream open,
                ## until the request future is completed
                await response_future

                ## await end-of-parse
                # await thr_future

            if __debug__:
                logger.debug("process_response: parse_response => %r", thr_future)
        except Exception:
            etyp, exc, tb = sys.exc_info()
            set_future_exception(response_future, exc)
            self.controller.present_exception(etyp, exc, tb)
            await stream.aclose()
            raise

    def parse_response(self, stream: AsyncSegmentChannel,
                       client_response: httpx.Response,
                       initial_request: httpx.Request):
        # bootstrap an asynchronous response processing call
        # from within a synchronous thread start function
        worker_loop = thread_loop.get()
        response_future = self.future
        if __debug__:
            logger.debug("parse_response: dispatch to parse_response_async")
        try:
            ## dispatching to the async parser, from within this synchronous thread runner
            ##
            ## this assumes the thread's loop was not already running
            rslt = worker_loop.run_until_complete(
                self.parse_response_async(
                    stream,
                    client_response,
                    initial_request
                ))
            if __debug__:
                logger.debug("parse_response: parse_response_async => %s", rslt)
            return rslt
        except Exception:
            etyp, exc, tb = sys.exc_info()
            self.controller.present_exception(etyp, exc, tb)
            set_future_exception(response_future, exc)

    async def parse_response_async(self,
                                   stream: AsyncSegmentChannel[bytes],
                                   client_response: httpx.Response,
                                   initial_request: httpx.Request):
        ## parse a server response asynchronously
        response = ''
        response_future = self.future
        try:
            response_type = await self.get_response_type(client_response, stream)
            if response_type is None:
                response_headers = client_response.headers
                # Implementation Note
                #
                # The response header names will be received here as downcased,
                # mainly in the syntax presented by the v20 API servers
                #
                content_info = response_headers["content-type"] if "content-type" in response_headers else None
                content_type = content_info.split(';', maxsplit=1)[0] if content_info else None
                if content_type == REST_CONTENT_TYPE:
                    # unexpected JSON formatted response
                    response_type = ApiErrorResponse

            if response_type:
                builder = ModelBuilder(response_type)
                ## main parser - deserialize an object for a model class determined
                ## per the server response status code
                ##
                ## the resulting object may indicate one of a set of formatted
                ## exception responses per individual endpoint requests, or a
                ## 'success' response object
                ##
                ## the 'success' response type may itself represent an abstract
                ## model object class ...
                ##
                # delay = sys.getswitchinterval()

                async for event, value in ijson.basic_parse_async(stream, use_float=True, multiple_values=True):
                    # if __debug__:
                    #     logger.debug("parse_response_async: event %s => %r", event, value)

                    # try:
                    await builder.aevent(event, value)
                    # except ValidationError:
                    #     raise

                    if builder.finalized:
                        response = builder.instance
                        if __debug__:
                            logger.debug("parse_response_async: parsed %r", response)
                        # process the response object
                        response_task = self.controller.add_task(self.dispatch_response(response, client_response, initial_request))
                        await response_task
                        if stream.eof or client_response.is_closed:
                            # endpoint provided a single REST response, or this is a streaming
                            # endpoint with a closed response channel
                            return
                        else:
                            # create a new builder for processing subsequent response objects,
                            # generally for a streaming endpoint
                            builder = ModelBuilder(response_type)
            elif response_type is False:
                await self.dispatch_response(False, client_response, initial_request)
                return
            else:
                #
                # not an expected server response and not a JSON response
                #
                # the response may have originated from a proxy server
                #
                status = client_response.status_code
                data: bytes = await stream.read()
                charset = client_response.charset_encoding
                content = data.decode(charset) if charset else data.decode()
                if __debug__:
                    logger.warning(
                        "parse_response_async: unexpected %s response %d (truncated) %r...",
                        content_type or "<content type undefined>",
                        status, content[:70]
                    )
                response = UnknownErrorResponse(
                    error_code=status,
                    reason=client_response.reason_phrase,
                    content_type=content_type,
                    content=content
                )
                await self.dispatch_response(response, client_response, initial_request)
        except Exception:
            # parse failed, return
            etyp, exc, tb = sys.exc_info()
            self.controller.present_exception(etyp, exc, tb)
            await stream.aclose()
            set_future_exception(response_future, exc)
            return


class ApiRestRequest(ApiRequest[T_response, T_value], ABC):

    @classmethod
    @abstractmethod
    def response_iter(cls, response: T_response) -> Iterator[T_value]:
        raise NotImplementedError(cls.response_iter)

    async def aeach_object(self, interval: Union[int, float] = 0) -> AsyncIterator[T_value]:
        future = self.future
        try:
            await future
        except aio.CancelledError:
            return
        except:
            raise
        exc = future.exception()
        if exc:
            raise exc
        for inst in self.__class__.response_iter(future.result()):
            yield inst
            ## ensuring it's a non-blocking iterator
            await aio.sleep(interval)


class ApiIterativeRequest(ApiRequest[T_response, T_value], ABC):

    response_queue: Annotated[SimpleQueue[T_response], ApplicationField(..., default_factory=SimpleQueue)]

    async def aeach_response(self, interval: Union[int, float] = 0) -> AsyncIterator[T_response]:
        # non-blocking iterator for response member objects @ stream I/O
        q = self.response_queue
        f = self.future
        while True:
            with suppress(Empty):
                yield q.get(timeout=0)
            if f.done() and q.empty():
                return
            else:
                await aio.sleep(interval)

    def append_response(self, response: type[ApiObject]):
        self.response_queue.put(response)

    @abstractmethod
    def chain_response_p(self, client_response: httpx.Response):
        raise NotImplementedError(self.chain_response_p)

    @abstractmethod
    def get_next_url(self,
                     response: Union[ApiObject, Literal[False]],
                     client_response: httpx.Response) -> Optional[str]:
        raise NotImplementedError(self.get_next_url)

    async def dispatch_response(self,
                                response: Union[ApiObject, Literal[False]],
                                client_response: httpx.Response,
                                initial_request: httpx.Request):
        if self.chain_response_p(client_response):
            self.append_response(response)
        else:
            if client_response.status_code < 300:
                ## append a final response object
                self.append_response(response)
            ## dispatch to set the response future
            return await super().dispatch_response(response, client_response, initial_request)
        ## dispatch to any next request
        future = self.future
        if not future.done():
            next_url = self.get_next_url(response, client_response)
            if next_url:
                if __debug__:
                    logger.info("Processing next request")

                ## updating the initial_request object for the next URL
                initial_request.url = httpx.URL(next_url)

                async def process_next(self: Self, next_request, future):
                    ## coroutine for request=>response model with modified initial_request
                    ## to be run under the same loop as self.future, typically the loop where
                    ## the initial async HTTP client was created
                    if future.done():
                        return
                    async with self.request_stream(next_request) as linked_response:
                        await self.process_response(linked_response, next_request)

                loop = self.controller.main_loop
                cf: cofutures.Future = aio.run_coroutine_threadsafe(process_next(self, initial_request, future), loop=loop)
                self.future.add_done_callback(lambda _: cf.cancel())
                # poll until next request has completed
                interval = sys.getswitchinterval()
                while not cf.done():
                    try:
                        return cf.result(0)
                    except cofutures.TimeoutError:
                        await aio.sleep(interval)
            else:
                logger.warning("Received no next URL for linked response in %r", self)


class ApiLinkedRequest(ApiIterativeRequest[T_response, T_value], ABC):

    def chain_response_p(self, client_response: httpx.Response):
        ## header syntax: see below
        return "link" in client_response.headers

    def get_next_url(self,
                     response: Union[ApiObject, Literal[False]],
                     client_response: httpx.Response) -> Optional[str]:
        link = client_response.headers.get("link", None)
        if link:
            m = re.match(re.compile(r"<(.*)>"), link)
            if m:
                return m.group(1)
            else:
                logger.critical("Received link header without link URL %r", self)


T_abstract_co = TypeVar("T_abstract_co", bound=AbstractApiObject, covariant=True)


class ApiStreamRequest(ApiIterativeRequest[T_abstract_co, T_abstract_co], ABC):

    def request_host(self) -> str:
        return self.host.stream_host

    def chain_response_p(self, client_response: httpx.Response):
        return not client_response.is_closed

    async def dispatch_response(self,
                                response: Union[ApiObject, Literal[False]],
                                client_response: httpx.Response,
                                initial_request: httpx.Request):
        if self.chain_response_p(client_response):
            self.append_response(response)
        else:
            if client_response.status_code < 300:
                ## append a final response object
                self.append_response(response)
            ## dispatch to set the response future
            return await super().dispatch_response(response, client_response, initial_request)

    async def aeach_object(self, interval: int | float = 0) -> AsyncIterator[T_abstract_co]:
        async for obj in self.aeach_response(interval):
            yield obj
