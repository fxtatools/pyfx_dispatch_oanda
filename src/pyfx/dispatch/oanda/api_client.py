## ApiClient, originally based on code generated with OpenAPI Generator

from enum import Enum, StrEnum
import asyncio as aio
import datetime
from numbers import Real
import logging
from typing import Any, Awaitable, Mapping, Optional, Sequence, Union
from typing_extensions import AsyncGenerator, TypeVar

from urllib.parse import quote_from_bytes

from .exceptions import RequestValueError
from .exec_controller import ExecController
from .credential import Credential
from .transport.data import ApiObject
from .configuration import Configuration
from . import rest
from .request_constants import RequestMethod
from .hosts import FxHostInfo

from .util.naming import exporting

logger = logging.getLogger(__name__)

__all__ = ("ApiClient",)

To_co = TypeVar("To_co", covariant=True)


class BoolStr(StrEnum):
    TRUE= "true"
    FALSE = "false"

def ensure_str(value) -> str:
    # utility function for query path encoding
    #
    # caveats
    # - query paths in the v20 API will not need special quoting
    # - query paths in the v20 API will not Include sequence elements
    if isinstance(value, str):
        return value
    elif isinstance(value, Real):
        return str(value)
    elif isinstance(value, bool):
        return BoolStr.TRUE if value else BoolStr.FALSE
    elif isinstance(value, Credential):
        return value.get_secret_value()
    else:
        return str(value)


class ApiClient(object):
    """API client

    Originally based on Python source code produced with OpenAPI Generator

    :param configuration: Configuration object for this client
    :param header_name: a header to pass when making calls to the API.
    :param header_value: a header value to pass when making calls to
        the API.
    :param cookie: a cookie to include in the header when making calls
        to the API
    """

    # fmt: off
    __slots__ = ("config", "controller", "encoder", "loop", "rest_client",)
    # fmt: on

    config: Configuration
    controller: ExecController
    '''Reference to a managing ExecController, typically an ApiController'''

    loop: aio.AbstractEventLoop
    rest_client: rest.RESTClientObject

    def __init__(self, controller: ExecController):
        self.config = controller.config
        self.loop = controller.main_loop
        self.rest_client = rest.RESTClientObject(controller)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.aclose()

    async def aclose(self):
        try:
            await self.rest_client.aclose()
        except:
            pass


    async def call_api(self,  # fmt: off
                       resource_path: str,
                       method: RequestMethod,
                       *, path_params: Optional[Mapping[str, Any]] = None,
                       query_params: Optional[Mapping[str, Any]] = None,
                       header_params: Optional[Mapping[str, Any]] = None,
                       body: Optional[ApiObject] = None,
                       response_types_map: Optional[Mapping[int, type[ApiObject]]] = None,
                       collection_formats: Optional[Mapping[str, str]] = None,
                       streaming: bool = False,
                       receiver: Optional[AsyncGenerator[Any, bytes]] = None,
                       future: Optional[aio.Future[To_co]] = None,
                       ) -> Awaitable[Optional[To_co]]:
        # fmt: on
        if __debug__:
            if streaming and not receiver:
                logger.critical(
                    "Streaming request without receiver: %s %s", method, resource_path
                )

        if header_params:
            header_params = self.serialize_headers(header_params)

        # path parameters
        if path_params:
            resource_path = resource_path.format(
                **{k: ensure_str(v) for k, v in path_params.items()}
            )

        body_text = None if body is None else body.to_json_bytes()

        ## generalization for fxPractice and fxLive endpoints
        # fmt: off
        host_info = (FxHostInfo.fxPractice if self.config.fxpractice else FxHostInfo.fxLive)
        ## generalization for endpoints using streaming or conventional REST responses
        host = host_info.stream_host if streaming else host_info.rest_host
        base_url = host + resource_path
        # fmt: on

        if query_params:
            # fmt: off
            base_url += "?" + await self.serialize_query(query_params, collection_formats)
            # fmt: on

        ## send the request and return the API object
        return await self.rest_client.request(
            method,
            base_url,
            response_types_map,  # type: ignore
            headers=header_params,
            body=body_text,
            receiver=receiver,
            future=future,
        )

    def serialize_headers(self, headers: Mapping[str, Any]):
        return {k: ensure_str(v) for k, v in headers.items()}

    async def serialize_quoting(
        self,
        value: Union[
            str, bytes, Enum, Real, bool, datetime.datetime, ApiObject, Sequence
        ],
    ) -> Awaitable[str]:
        ## originally 'sanitize_for_serialization', subsequently adapted
        if isinstance(value, str):
            return await self.serialize_quoting(value.encode())
        elif isinstance(value, bytes):
            return quote_from_bytes(value, safe=b"")  # type: ignore
        elif isinstance(value, Enum):
            ## assumption: enum values should not need quoting
            return value.value
        elif isinstance(value, Real):
            return str(value)  # type: ignore
        elif isinstance(value, bool):
            return BoolStr.TRUE if value == True else BoolStr.FALSE  # type: ignore
        elif isinstance(value, datetime.datetime):
            ## alternately a pandas timestamp
            return value.isoformat(timespec="milliseconds")  # type: ignore
        elif isinstance(value, ApiObject):
            return value.to_json_str()  # type: ignore
        elif isinstance(value, Sequence):
            return ",".join([await self.serialize_quoting(obj) for obj in value])  # type: ignore
        elif isinstance(value, Mapping):
            raise RequestValueError("Received an unserialized mapping", value)
        else:
            raise RequestValueError("Unknown value", value)

    async def serialize_query(self, params, collection_formats):
        # Used for query_params for the URL encoding
        return "&".join(
            [k + "=" + await self.serialize_quoting(v) for k, v in params.items()]
        )


__all__ = exporting(__name__, ...)
