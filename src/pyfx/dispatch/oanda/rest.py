
import asyncio as aio
import ijson
import httpx
import logging
import re
from typing import Any, Awaitable, Callable, Mapping, Optional
from typing_extensions import AsyncGenerator, TypeVar

from .util.aio import chain_cancel_callback

from .api.transport_client import TransportClient

from .io import AsyncSegmentChannel
from .exec_controller import thread_loop
from .response_common import ResponseInfo, REST_CONTENT_TYPE
from .transport.data import ApiObject
from .exceptions import ApiException
from .request_constants import RequestMethod
from .parser import ModelBuilder

logger = logging.getLogger(__name__)

UTF8_RE_MATCH: re.Pattern = re.compile(r"\s*charset=[Uu][Tt][Ff]-8")
CHARSET_RE_GROUP: re.Pattern = re.compile(r"\s*charset=(\S+)")


T_co = TypeVar("T_co", bound=ApiObject)

##
## utils
##
def th_set_future_exception(future: aio.Future, exception: Exception) -> Optional[aio.Handle]:
    if not future.done():
        loop = future.get_loop()
        if aio.get_running_loop() is loop:
            future.set_exception(exception)
        else:
            return loop.call_soon_threadsafe(future.set_exception, exception)

def th_set_future_result(future: aio.Future, result: Any) -> Optional[aio.Handle]:
    if not future.done():
        loop = future.get_loop()
        if aio.get_running_loop() is loop:
            future.set_result(result)
        else:
            return loop.call_soon_threadsafe(future.set_result, result)



class RESTClientObject(TransportClient):
    # request-oriented implementation for ApiClient
    #
    # adapted after an implemenation produced with OpenAPI Generator

    async def request(self, method: RequestMethod, url: str,
                      response_types_map: Mapping[int, type[ApiObject]], *,
                      headers: Optional[Mapping[str, str]] = None,
                      body: Optional[str] = None,
                      receiver: Optional[AsyncGenerator[Any, bytes]] = None,
                      future: Optional[aio.Future[T_co]] = None
                      ) -> Awaitable[Optional[T_co]]:

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

        request_method = bytes(method)
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

            status = client_response.status_code
            reason = client_response.reason_phrase

            response_headers = client_response.headers

            content_type = response_headers["content-type"].split(";")[0].rstrip() if "content-type" in response_headers else None
            content_encoding = client_response.charset_encoding

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
                        th_set_future_exception(future, exc)
                finally:
                    if __debug__:
                        logger.debug("request [stream]: Returning")
                    await receiver.aclose()
            else:
                ## dispatch to an async component method for the REST response
                response_future = future or aio.Future[ApiObject]()
                if not response_future.done():
                    proc_coro = self.process_response(
                        response_future, client_response, response_types_map,
                        content_type, content_encoding
                        )
                    task: aio.Task = self.controller.add_task(proc_coro)
                    if __debug__:
                        ## Implementation Note: The request URL won't be logged here,
                        ## as it may contain a private account ID. The URL prototype
                        ## for the request may have been logged by the caller
                        logger.debug("request: Procesing response")
                    chain_cancel_callback(task, response_future)
                    chain_cancel_callback(response_future, task)
                    ## await the parser task
                    await task
                if future:
                    return None
                else:
                    await task
                    await response_future
                    return response_future.result()

    async def process_response(self, response_future: aio.Future, client_response: httpx.Response,
                               response_types_map: Mapping[int, type[ApiObject]],
                               content_type: str, content_encoding: Optional[str] = None):

        try:
            status = client_response.status_code
            response_type = response_types_map.get(status)

            async with AsyncSegmentChannel[bytes]() as stream:
                response_future.add_done_callback(lambda _: stream.close())
                if __debug__:
                    logger.debug("process_response: dispatch to parse_response thread")
                thr_future: aio.Future = self.controller.dispatch(
                    self.parse_response, response_future, stream, content_type, response_type, client_response
                    )

                if client_response.is_closed:
                    logger.critical("Received a closed response: %r @ %r", stream, self)
                    return

                async for chunk in client_response.aiter_bytes():
                    await stream.feed(chunk)
                ## feed EOF
                await stream.feed(b'', True)
                ## await end-of-parse, keeping the stream open meanwhile
                await thr_future
                if __debug__:
                    logger.debug("process_response: parse_response => %r", thr_future)
        except Exception as exc:
            await stream.aclose()
            th_set_future_exception(response_future, exc)

    def parse_response(self, response_future: aio.Future,
                       stream: AsyncSegmentChannel,
                       content_type: str, response_type: type[ApiObject],
                       client_response: httpx.Response):
        worker_loop = thread_loop.get()
        if __debug__:
            logger.debug("parse_response: dispatch to parse_response_async")
        try:
            ## dispatching to the async parser, from within this synchronous thread runner
            rslt = worker_loop.run_until_complete(self.parse_response_async(response_future, stream, content_type, response_type, client_response))
            if __debug__:
                logger.debug("parse_response: parse_response_async => %s", rslt)
            return rslt
        except Exception as exc:
            th_set_future_exception(response_future, exc)

    async def parse_response_async(self, response_future: aio.Future,
                                   stream: AsyncSegmentChannel[bytes],
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
                response: bytes = await stream.read()
                charset = client_response.charset_encoding
                response = response.decode(charset) if charset else response.decode()
                if __debug__:
                    logger.warning("parse_response_async: unexpected non-JSON response %r...", response[:70])
        except Exception as exc:
            ## parse failed, return
            th_set_future_exception(response_future, exc)
            return

        status = client_response.status_code
        if status and 200 <= status <= 299:
            th_set_future_result(response_future, response)
        else:
            ## set an exception indicating the server error response
            reason = client_response.reason_phrase
            api_exc = ApiException(status=status, reason=reason, response=response,
                                   content_type=content_type)
            th_set_future_exception(response_future, api_exc)

__all__ = ("RESTClientObject",)
