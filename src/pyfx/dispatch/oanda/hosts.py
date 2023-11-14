# common host information for OANDA v20 fxTrade and fxPractice endpoints

from typing_extensions import ClassVar
import encodings.idna
from .mapped_enum import MappedEnum


class EndpointBase(str, MappedEnum):
    """Host base URLs for fxTrade REST and Streaming endpoints"""
    # more info: https://developer.oanda.com/rest-live-v20/development-guide/
    fxpractice_rest = "https://api-fxpractice.oanda.com"
    fxpractice_streaming = "https://stream-fxpractice.oanda.com"

    fxlive_rest = "https://api-fxtrade.oanda.com"
    fxlive_streaming = "https://stream-fxtrade.oanda.com"


class FxHost:
    """Host definition for fxTrade v20 endpoints"""
    __slots__ = ("rest_host", "stream_host", "rest_host_bytes", "stream_host_bytes")

    rest_host: str
    rest_host_bytes: bytes
    stream_host: str
    stream_host_bytes: bytes
    api_path: ClassVar[str] = "/v3"

    def __init__(self, rest_host: str, stream_host: str):
        self.rest_host = rest_host
        self.rest_host_bytes = encodings.idna.ToASCII(rest_host)
        self.stream_host = stream_host
        self.stream_host_bytes = encodings.idna.ToASCII(stream_host)

    def __eq__(self, obj) -> bool:
        if id(self) is id(obj):
            return True
        other_cls = obj.__class__
        if issubclass(other_cls, MappedEnum):
            return self.__eq__(obj.value)
        elif not issubclass(other_cls, self.__class__):
            return False
        elif obj.rest_host == self.rest_host and obj.stream_host == self.stream_host:
            return True
        else:
            return False

    def __hash__(self) -> int:
        return hash((self.rest_host, self.stream_host,))

# class FxHostInfo(enum):


class FxHostInfo(MappedEnum):
    """Host definitions for fxTrade Practice and fxTrade Live endpoints"""

    fxPractice: FxHost = FxHost(
        rest_host=EndpointBase.fxpractice_rest + FxHost.api_path,
        stream_host=EndpointBase.fxpractice_streaming + FxHost.api_path
    )
    fxLive: FxHost = FxHost(
        rest_host=EndpointBase.fxlive_rest + FxHost.api_path,
        stream_host=EndpointBase.fxlive_streaming + FxHost.api_path
    )

    def __eq__(self, obj) -> bool:
        if id(self) is id(obj):
            return True
        else:
            return obj.__eq__(self.value)

    @property
    def rest_host(self):
        return self.value.rest_host

    @property
    def stream_host(self):
        return self.value.stream_host

    @property
    def rest_host_bytes(self):
        return self.value.rest_host_bytes

    @property
    def stream_host_bytes(self):
        return self.value.stream_host_bytes


__all__ = ("EndpointBase", "FxHost", "FxHostInfo",)
