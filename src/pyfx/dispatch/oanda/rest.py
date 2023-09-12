# coding: utf-8

import asyncio as aio
import io
import json
import logging
import ssl

import httpx
from urllib.parse import urlencode

from .exceptions import ApiException, ApiValueError
from .configuration import Configuration
from .request_constants import RequestMethod

logger = logging.getLogger(__name__)

class RESTResponse(io.IOBase):

    def __init__(self, resp: httpx.Response, data):
        self.http_response = resp
        self.status = resp.status_code
        self.reason = resp.reason_phrase
        self.data = data

    def getheaders(self):
        """Returns a CIMultiDictProxy of the response headers."""
        return self.http_response.headers

    def getheader(self, name, default=None):
        """Returns a given response header."""
        return self.http_response.headers.get(name, default)


class RESTClientObject(object):

    def __init__(self, loop: aio.AbstractEventLoop, configuration: Configuration):
        self._loop = loop

        maxconn = configuration.max_connections
        max_keepalive = configuration.max_keepalive_connections
        keepalive_expiry = configuration.keepalive_expiry

        limits = httpx.Limits(max_connections= maxconn,
                              max_keepalive_connections = max_keepalive,
                              keepalive_expiry=keepalive_expiry)

        ssl_context = ssl.create_default_context(cafile=configuration.ssl_ca_cert)
        if configuration.cert_file:
            ssl_context.load_cert_chain(
                configuration.cert_file, keyfile=configuration.key_file
            )

        if not configuration.verify_ssl:
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

        self.proxy = configuration.proxy
        self.proxy_headers = configuration.proxy_headers

        transport = httpx.AsyncHTTPTransport(http2=True, proxy=configuration.proxy,
                                             socket_options=configuration.socket_options,
                                             trust_env=True, retries=configuration.retries,
                                             limits=limits, verify=ssl_context)

        ses = httpx.AsyncClient(transport = transport)
        self.session = ses

    @property
    def session(self) -> httpx.AsyncClient:
        return self._session

    @session.setter
    def session(self, session: httpx.AsyncClient):
        self._session = session

    @property
    def closed(self) -> bool:
        return self.session.is_closed

    async def close(self):
        if not self.closed:
            await self.session.aclose()

    async def request(self, method: RequestMethod, url: str, query_params=None, headers=None,
                      body=None, post_params=None, _preload_content=True,
                      _request_timeout=None):
        """Execute request

        :param method: http request method
        :param url: http request url
        :param query_params: query parameters in the url
        :param headers: http request headers
        :param body: request json body, for `application/json`
        :param post_params: request post parameters,
                            `application/x-www-form-urlencoded`
                            and `multipart/form-data`
        :param _preload_content: this is a non-applicable field for
                                 the AiohttpClient.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        """
        if post_params and body:
            raise ApiValueError(
                "body parameter cannot be used with post_params parameter."
            )

        post_params = post_params or {}
        headers = headers or {}
        # url already contains the URL query string
        # so reset query_params to empty dict
        query_params = {}
        timeout = _request_timeout or 5 * 60

        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'

        args = {
            "method": method.name,
            "url": url,
            "timeout": timeout,
            "headers": headers
        }

        if self.proxy_headers:
            args["proxy_headers"] = self.proxy_headers

        if query_params:
            args["url"] += '?' + urlencode(query_params)

        # For `POST`, `PUT`, `PATCH`, and `DELETE`
        if method.isFormRequest():
            # Implementation Note:
            #
            # All form requests in the v20 API will use json encoding
            # in the request body
            if body:
                args['json'] = json.dumps(body)
            else:
                raise ApiException("No request body provided for %s request" % method.name, url)

        if __debug__:
            logger.debug("request %s %s", method.name, url)
        r = await self.session.request(**args)
        if _preload_content:
            if __debug__:
                logger.debug("preload %s %s", method.name, url)

            data = await r.aread()
            await r.aclose()
            r = RESTResponse(r, data)

            # log response body
            if __debug__:
                logger.debug("parsed response: %s", r.data)

            if not 200 <= r.status <= 299:
                raise ApiException(http_resp=r)

        return r

    async def get_request(self, url, headers=None, query_params=None,
                  _preload_content=True, _request_timeout=None):
        return (await self.request(RequestMethod.GET, url,
                                   headers=headers,
                                   _preload_content=_preload_content,
                                   _request_timeout=_request_timeout,
                                   query_params=query_params))

    async def head_request(self, url, headers=None, query_params=None,
                   _preload_content=True, _request_timeout=None):
        return (await self.request(RequestMethod.HEAD, url,
                                   headers=headers,
                                   _preload_content=_preload_content,
                                   _request_timeout=_request_timeout,
                                   query_params=query_params))

    async def options_request(self, url, headers=None, query_params=None,
                      post_params=None, body=None, _preload_content=True,
                      _request_timeout=None):
        return (await self.request(RequestMethod.OPTIONS, url,
                                   headers=headers,
                                   query_params=query_params,
                                   post_params=post_params,
                                   _preload_content=_preload_content,
                                   _request_timeout=_request_timeout,
                                   body=body))

    async def delete_request(self, url, headers=None, query_params=None, body=None,
                     _preload_content=True, _request_timeout=None):
        return (await self.request(RequestMethod.DELETE, url,
                                   headers=headers,
                                   query_params=query_params,
                                   _preload_content=_preload_content,
                                   _request_timeout=_request_timeout,
                                   body=body))

    async def post_request(self, url, headers=None, query_params=None,
                   post_params=None, body=None, _preload_content=True,
                   _request_timeout=None):
        return (await self.request(RequestMethod.POST, url,
                                   headers=headers,
                                   query_params=query_params,
                                   post_params=post_params,
                                   _preload_content=_preload_content,
                                   _request_timeout=_request_timeout,
                                   body=body))

    async def put_request(self, url, headers=None, query_params=None, post_params=None,
                  body=None, _preload_content=True, _request_timeout=None):
        return (await self.request(RequestMethod.PUT, url,
                                   headers=headers,
                                   query_params=query_params,
                                   post_params=post_params,
                                   _preload_content=_preload_content,
                                   _request_timeout=_request_timeout,
                                   body=body))

    async def patch_request(self, url, headers=None, query_params=None,
                    post_params=None, body=None, _preload_content=True,
                    _request_timeout=None):
        return (await self.request(RequestMethod.PATCH, url,
                                   headers=headers,
                                   query_params=query_params,
                                   post_params=post_params,
                                   _preload_content=_preload_content,
                                   _request_timeout=_request_timeout,
                                   body=body))
