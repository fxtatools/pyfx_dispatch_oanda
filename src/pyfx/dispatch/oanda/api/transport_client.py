"""TransportClient base class (API client support)"""

from contextlib import suppress
import httpx
from immutables import Map
import ssl

from ..exec_controller import ExecController
from ..response_common import REST_CONTENT_TYPE_BYTES


class TransportClient():
    """Client wrapper for HTTP requests

    TransportClient provides a generalization of the original REST client produced
    with OpenAPI Generator.

    """
    __slots__ = "transport", "client", "controller"

    transport: httpx.AsyncHTTPTransport
    client: httpx.AsyncClient
    controller: ExecController

    def __init__(self, controller: ExecController):
        self.controller = controller
        config = controller.config

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
        proxy = httpx.Proxy(proxy_in) if proxy_in is not None and not isinstance(proxy_in, httpx.Proxy) else proxy_in

        headers = Map({
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
                                   timeout=config.request_timeout,
                                   headers=headers)
        self.client = client

    async def aclose(self):
        # Implementation Note: For connection pooling with HTTP/2
        # via HTTPX and HTTPCore, the same transport and client
        # objects should be used throughout each application
        # session.
        #
        # Similarly, aclose should be called at the end of the
        # application session. This is managed, for instance,
        # in the RequestController.async_context() context
        # manager.
        #
        with suppress(Exception):
            if hasattr(self, "client"):
                await self.client.aclose()
            if hasattr(self, "transport"):
                await self.transport.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, tb):
        await self.aclose()


__all__ = ("TransportClient",)
