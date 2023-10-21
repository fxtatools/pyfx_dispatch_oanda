
import asyncio as aio
import ijson
import httpx
import logging
import os
import re
import ssl
from typing import Any, Awaitable, Mapping, Optional
from types import MappingProxyType
from typing_extensions import AsyncGenerator

from .io import AsyncSegmentChannel
from .exec_controller import ExecController, thread_loop
from .response_common import ResponseInfo, REST_CONTENT_TYPE, REST_CONTENT_TYPE_BYTES
from .transport.data import ApiObject
from .exceptions import ApiException
from .request_constants import RequestMethod
from .parser import ModelBuilder

logger = logging.getLogger(__name__)

UTF8_RE_MATCH: re.Pattern = re.compile(r"\s*charset=[Uu][Tt][Ff]-8")
CHARSET_RE_GROUP: re.Pattern = re.compile(r"\s*charset=(\S+)")


def set_future_exception(future: aio.Future, exception: Exception):
    future.get_loop().call_soon_threadsafe(future.set_exception, exception)


class RESTClientObject():
    ## per-request generalization for ApiClient

    transport: httpx.AsyncHTTPTransport
    client: httpx.AsyncClient
    controller: ExecController

    def __init__(self, controller: ExecController):
        self._loop = controller.main_loop
        config = controller.config
        self.config = config
        self.controller = controller

        maxconn = config.max_connections
        max_keepalive = config.max_keepalive_connections
        keepalive_expiry = config.keepalive_expiry

        limits = httpx.Limits(max_connections=maxconn,
                              max_keepalive_connections=max_keepalive,
                              keepalive_expiry=keepalive_expiry)

        ssl_context = ssl.create_default_context(cafile=config.ssl_ca_cert)

        if config.ssl_cert_file:
            ssl_context.load_cert_chain(
                config.ssl_cert_file, keyfile=config.ssl_key_file
            )

        if not config.verify_ssl:
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

        proxy_in = config.proxy
        if proxy_in is None:
            proxy_in = os.environ["https_proxy"] if "https_proxy" in os.environ else os.environ["HTTPS_PROXY"] if "HTTPS_PROXY" in os.environ else None
        proxy = httpx.Proxy(proxy_in) if proxy_in and not isinstance(proxy_in, httpx.Proxy) else proxy_in

        headers = MappingProxyType({
            b'Authorization': b'Bearer ' + config.access_token.encode(),
            b'Accept': REST_CONTENT_TYPE_BYTES,
            b'User-Agent': b'pyfx.dispatch/1.0.1/python',
        })

        transport = httpx.AsyncHTTPTransport(http2=True, proxy=proxy,
                                             socket_options=config.socket_options,
                                             trust_env=True, retries=config.retries,
                                             limits=limits, verify=ssl_context)
        self.transport = transport

        ## enabling follow_redirects after response 307, "Temporary Redirect"
        ## with the v20 demo server
        ##
        ## this client will be reused for every request
        client = httpx.AsyncClient(transport=transport,
                                   follow_redirects=True,
                                   headers=headers)
        self.client = client

    def __del__(self):
        loop = self.controller.main_loop
        if not loop.is_closed():
            loop.run_until_complete(self.aclose())

    @property
    def client(self) -> httpx.AsyncClient:
        return self._client

    @client.setter
    def client(self, session: httpx.AsyncClient):
        self._client = session

    async def aclose(self):
        ## Implementation Note: The same self.session value should be used
        ## throughout each application session, mainly to ensure HTTP/2
        ## support can be implemented in a "Most optimal" way, e.g
        ## for connection reuse if not also for request pipelining
        if hasattr(self, "transport"):
            await self.transport.aclose()
        if hasattr(self, "client"):
            await self.client.aclose()

    async def request(self, method: RequestMethod, url: str,
                      response_types_map: Mapping[int, type[ApiObject]], *,
                      headers: Optional[Mapping[str, str]] = None,
                      body: Optional[str] = None,
                      receiver: Optional[AsyncGenerator[Any, bytes]] = None,
                      future: Optional[aio.Future[ApiObject]] = None
                      ) -> Awaitable[Optional[ApiObject]]:

        """Send an HTTP request and return an ApiObject

        :param method: http request method
        :param url: http request url, including host, path, and query string, URL encoded
        :param response_types_map: Mapping of HTTP response code to ApiObject classes
        :param headers: http request headers, including the supported content type
                application/json
        :param body: JSON-encodable request body, if applicable

        If a receiving async generator is provided, returns the provided generator,
        else returns a deserialized ApiObject
        """

        request_method = method.name
        request_headers = headers
        request_url = url

        request_json = None
        if __debug__:
            if method.isFormRequest():
                assert isinstance(body, str), "Request body is not a string"
            logger.debug("request: sending request %s %s", method.name, url)

        status = None
        reason = None
        async with self.client.stream(request_method, request_url,
                                      headers=request_headers,
                                      json=request_json) as client_response:
            if __debug__:
                logger.debug("request: processing response %s %s", method.name, url)

            encoding = client_response.charset_encoding
            status = client_response.status_code
            reason = client_response.reason_phrase


            response_headers = client_response.headers
            content_info = response_headers["Content-Type"].split(";") if "Content-Type" in response_headers else None
            content_type = content_info[0].rstrip() if content_info else None
            if content_info:
                ## assumptions for client access to the v20 fxTrade servers:
                ## - for REST requests, content_info[0]=="application/json", content_info[1]==" charset=UTF-8",
                ## - for streaming requests, content_info[0] == "application/octet-stream", len(content_info) == 1
                if len(content_info) is int(1):
                    content_encoding = None
                else:
                    content_end = content_info[1]
                    if UTF8_RE_MATCH.match(content_end):
                        content_encoding = None
                    else:
                        m = CHARSET_RE_GROUP.match(content_end)
                        content_encoding = m.group(1)
            else:
                content_encoding = None

            if receiver:
                ## This call section would provide support for the streaming endpoints
                ## in the OANDA v20 fxTrade API. The receiver should represent an
                ## asynchronous generator. The generator will receive successive byte
                ## sequences from this function, via asend.
                ##
                ## In a successful response for a streaming endpoint, the server
                ## will generally send sucessive chunks of fully encoded JSON object
                ## representations.
                ##
                ## For each of the two streaming endpoints in the v20 API, a method is
                ## provided in DefaultApi such that will provide a generator incorporated
                ## with a JSON parser and callback infrastructure. The generator will
                ## receive byte sequences form the following iterator
                info = ResponseInfo(response_types_map, status, reason,
                                    response_headers, content_type, content_encoding)
                if __debug__:
                    logger.debug("request [stream]: Initializing receiver")
                try:
                    await receiver.asend(None)
                    if __debug__:
                        logger.debug("request [stream]: Sending response information")
                    await receiver.asend(info)
                    last = None
                    if __debug__:
                        logger.debug("request [stream]: Sending response bytes")
                    async for chunk in client_response.aiter_bytes():
                        await receiver.asend(chunk)
                    if future:
                        try:
                            future.set_result(True)
                        except:
                            logger.critical("request [stream]: Failed to set future result: %r", future)
                            raise
                    return
                except Exception as exc:
                    if future:
                        set_future_exception(future, exc)
                finally:
                    if __debug__:
                        logger.debug("request [stream]: Returning")
                    await receiver.aclose()
            else:
                ## dispatch to an async component method for the REST response
                response_future = future or aio.Future[ApiObject]()
                if not response_future.done():
                    proc_coro = self.process_response(response_future, client_response, response_types_map, content_type)
                    task = self.controller.main_loop.create_task(proc_coro)
                    if __debug__:
                        ## Implementation Note: The request URL won't be logged here,
                        ## as it may contain a private account ID. The URL prototype
                        ## for the request may have been logged by the caller
                        logger.debug("request: Procesing response")
                    await response_future
                    await task
                return None if future else response_future.result()

    async def process_response(self, response_future: aio.Future, client_response: httpx.Response,
                               response_types_map: Mapping[int, type[ApiObject]],
                               content_type: str):

        try:
            status = client_response.status_code
            response_type = response_types_map.get(status)

            async with AsyncSegmentChannel[bytes]() as stream:
                async for chunk in client_response.aiter_bytes():
                    await stream.feed(chunk)
                ## feed EOF
                await stream.feed(b'', True)
                response_future.add_done_callback(lambda _: stream.close())
                if __debug__:
                    logger.debug("process_response: dispatch to parse_response thread")
                rslt = await self.controller.dispatch(self.parse_response, response_future, stream, content_type, response_type, client_response)
                if __debug__:
                    logger.debug("process_response: parse_response => %r", rslt)
        except Exception as exc:
            await stream.aclose()
            set_future_exception(response_future, exc)

    def parse_response(self, response_future: aio.Future,
                       stream: AsyncSegmentChannel,
                       content_type: str, response_type: type[ApiObject],
                       client_response: httpx.Response):
        loop = thread_loop.get()
        if __debug__:
            logger.debug("parse_response: dispatch to parse_response_async")
        try:
            ## dispatching to the async parser, from within this synchronous thread runner
            rslt = loop.run_until_complete(self.parse_response_async(response_future, stream, content_type, response_type, client_response))
            if __debug__:
                logger.debug("parse_response: parse_response_async => %s", rslt)
            return rslt
        except Exception as exc:
            set_future_exception(response_future, exc)

    async def parse_response_async(self, response_future: aio.Future,
                                   stream: AsyncSegmentChannel,
                                   content_type: str, response_type: type[ApiObject],
                                   client_response: httpx.Response):
        ## parse a server response asynchronously
        response = ''
        try:
            if response_type:
                builder = ModelBuilder(response_type)
                ## main parser - deserialize an object for a model class determined
                ## in the calling context, per the server response status code
                ##
                ## the resulting object may indicate one of a set of possible expected
                ## exception responses, for response codes >= 300 in the original
                ## response types map.
                async for event, value in ijson.basic_parse_async(stream, use_float=True):
                    # if __debug__:
                    #     logger.debug("parse_response_async: event %s => %r", event, value)
                    await builder.aevent(event, value)
                response = builder.instance
                if __debug__:
                    logger.debug("parse_response_async: parsed %r", response)
            elif content_type == REST_CONTENT_TYPE:
                ## parse any response content for an unexpected JSON-typed response
                async for toplevel in ijson.items_async(stream, ''):
                    response = toplevel
                    break
                if __debug__:
                    logger.warning("parse_response_async: unexpected JSON response %r", response)
            else:
                ## read any non-JSON response
                ##
                ## the response here may represent an intermediate proxy response,
                ## typically using an HTML content type
                response = stream.read()
                if __debug__:
                    logger.warning("parse_response_async: unexpected non-JSON response %r...", response[:70])
        except Exception as exc:
            ## parse failed, return
            set_future_exception(response_future, exc)
            return

        status = client_response.status_code
        if status and 200 <= status <= 299:
            try:
                self.controller.main_loop.call_soon_threadsafe(response_future.set_result, response)
            except Exception as exc:
                logger.critical("parse_response_async: Failed to initialize call to set result for future %r", response_future)
                raise
        else:
            ## set an exception indicating the server error response
            reason = client_response.reason_phrase
            api_exc = ApiException(status=status, reason=reason, response=response,
                                   content_type=content_type)
            set_future_exception(response_future, api_exc)
