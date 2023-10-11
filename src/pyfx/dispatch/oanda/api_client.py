## ApiClient, based on code generated with OpenAPI Generator

from enum import Enum
import asyncio as aio
import atexit
import datetime
from numbers import Real
import logging
from typing import Any, Awaitable, Mapping, Optional, Sequence, Union
from typing_extensions import AsyncGenerator, TypeAlias

from urllib.parse import quote

from .exec_controller import ExecController
from .transport import JsonLiteral, ApiObject
from .configuration import Configuration
from . import rest
from .request_constants import BoolStr, RequestMethod
from .hosts import FxHostInfo

from .util.naming import exporting

logger = logging.getLogger(__name__)

__all__ = ("ApiClient",)


## additional type definition for ApiClient
##
## forward reference will be resolvable once .data is loaded
## at the package scope
Serializable: TypeAlias = Union[JsonLiteral, Sequence, Mapping, ApiObject]


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

    # def __init__(self, loop: aio.AbstractEventLoop,
    #              configuration: Configuration):
    def __init__(self, controller: ExecController):
        self.config = controller.config

        self._loop = controller.main_loop

        self.rest_client = rest.RESTClientObject(controller)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    async def close(self):
        await self.rest_client.aclose()
        if hasattr(atexit, 'unregister'):
            atexit.unregister(self.close)

    @property
    def loop(self) -> aio.AbstractEventLoop:
        return self._loop

    def set_default_header(self, header_name, header_value):
        assert isinstance(header_name, str), "header_name is not a string"
        assert isinstance(header_value, str), "header_value is not a string"

    async def call_api(
            self, resource_path: str, method: RequestMethod, *,
            path_params=None, query_params=None, header_params=None,
            body: Optional[ApiObject] = None,
            response_types_map: Optional[Mapping[int, type[ApiObject]]] = None,
            collection_formats: Optional[Mapping[str, str]] = None,
            streaming: bool = False,
            receiver: Optional[AsyncGenerator[Any, bytes]] = None,
            future: Optional[aio.Future[ApiObject]] = None) -> Awaitable[Optional[ApiObject]]:

        if __debug__:
            if streaming and not receiver:
                logger.critical("Streaming request without receiver: %s %s", method, resource_path)

        if header_params:
            header_params = self.serialize_headers(header_params)

        # path parameters
        if path_params:
            path_params = self.serialize_params(path_params, collection_formats)
            resource_path = resource_path.format(**{k: quote(v, safe='') for k, v in path_params})

        if body:
            body = body.to_json_str()

        ## generalization for fxPractice and fxLive endpoints
        host_info = FxHostInfo.fxPractice if self.config.fxpractice else FxHostInfo.fxLive
        ## generalization for endpoints using streaming or conventional REST responses
        host = host_info.stream_host if streaming else host_info.rest_host
        base_url = host + resource_path

        if query_params:
            # query_params = self.sanitize_for_serialization(query_params)
            base_url += ("?" + self.serialize_query(query_params, collection_formats))

        ## send the request and return the API object
        return await self.rest_client.request(
            method, base_url, response_types_map,
            headers=header_params,
            body=body, receiver=receiver, 
            future=future)

    def serialize_headers(self, headers: Mapping[str, Any]):
        return {k: self.sanitize_for_serialization(v) for k, v in headers.items()}

    def sanitize_for_serialization(self, params: Serializable):
        """Builds a JSON POST object.

        If params is None, return None.
        If params is str, int, long, float, bool, return directly.
        If params is datetime.datetime, datetime.date
            convert to string in iso8601 format.
        If params is list, sanitize each element in the list.
        If params is dict, return the dict.
        If params is OpenAPI model, return the properties dict.

        :param params: The data to serialize.
        :return: The serialized form of data.
        """
        # print("!THUNK S %r" % (params,))
        if params is None:
            return None
        elif isinstance(params, Enum):
            return params.value
        elif isinstance(params, JsonLiteral):
            return params
        elif isinstance(params, (datetime.datetime, datetime.date)):
            return params.isoformat(timespec='seconds')
        elif isinstance(params, ApiObject):
            return params.model_dump_json(by_alias=True)
        elif isinstance(params, Sequence):
            return params.__class__(self.sanitize_for_serialization(sub_obj) for sub_obj in params)
        elif isinstance(params, Mapping):
            return {key: self.sanitize_for_serialization(val) for key, val in params.items()}
        else:
            return params

    def serialize_params(self, params, collection_formats):
        """Get parameters as list of tuples, formatting collections.

        :param params: Parameters as dict or list of two-tuples
        :param dict collection_formats: Parameter collection formats
        :return: Parameters as list of tuples, collections formatted
        """
        ## used for GET and POST params
        for k, v in params.items() if isinstance(params, Mapping) else params:  # noqa: E501
            if collection_formats and k in collection_formats:
                ## csv is the single query join syntax used in the v20 API
                ##
                ## Usage:
                ## - get_account_instruments
                ## - get_prices
                ## - get_transaction_range
                ## - list_orders
                ## - list_trades
                ## - list_transactions
                ## - stream_pricing
                yield (k, ",".join(self.sanitize_for_serialization(value) for value in v))
            else:
                yield (k, self.sanitize_for_serialization(v))

    # Used for query_params for the URL encoding
    def serialize_query(self, params, collection_formats):
        """Get parameters as list of tuples, formatting collections.

        :param params: Parameters as dict or list of two-tuples
        :param dict collection_formats: Parameter collection formats
        :return: URL query string (e.g. a=Hello%20World&b=123)
        """
        new_params = []
        for k, v in params.items() if isinstance(params, Mapping) else params:
            if isinstance(v, Real):
                v = str(v)
            if isinstance(v, bool):
                v = BoolStr.true if v else BoolStr.false
            if isinstance(v, str):
                new_params.append((k, quote(v, safe='')))
            if collection_formats and k in collection_formats:
                new_params.append(
                    (k, ",".join(quote(str(self.sanitize_for_serialization(value)), safe='') for value in v)))
            else:
                new_params.append((k, quote(str(self.sanitize_for_serialization(v)), safe='')))
        return "&".join(k + "=" + v for k, v in new_params)


__all__ = exporting(__name__, ...)
