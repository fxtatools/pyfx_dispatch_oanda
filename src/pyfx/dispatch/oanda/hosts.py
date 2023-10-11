# common host information for OANDA v20 fxTrade and fxPractice endpoints

from dataclasses import dataclass
from typing_extensions import ClassVar
from enum import StrEnum, Enum

from .util.naming import exporting

class EndpointBase(StrEnum):
    """Host base URLs for fxTrade REST and Streaming endpoints"""
    # the actual host URL to use may vary by request
    # - needs test
    # - test with the couple of streaming endpoints
    # - https://developer.oanda.com/rest-live-v20/development-guide/
    fxpractice_rest = "https://api-fxpractice.oanda.com"
    fxpractice_streaming = "https://stream-fxpractice.oanda.com"

    fxlive_rest = "https://api-fxtrade.oanda.com"
    fxlive_streaming = "https://stream-fxtrade.oanda.com"


@dataclass(frozen=True, slots=True)
class FxHost:
    """Host definition for fxTrade v20 endpoints"""
    rest_host: str
    stream_host: str
    api_path: ClassVar[str] = "/v3"
    
    def __eq__(self, obj) -> bool:
        other_cls = obj.__class__
        if issubclass(other_cls, Enum):
            return self.__eq__(obj.value)
        elif not issubclass(other_cls, self.__class__):
            return False
        elif obj.rest_host == self.rest_host and obj.stream_host == self.stream_host:
            return True
        else:
            return False

# class FxHostInfo(enum):
class FxHostInfo(Enum):
    """Host definitions for fxTrade Practice and fxTrade Live endpoints"""
    ## not seemingly working out as an "actual python enum"
    fxPractice: FxHost = FxHost(
        rest_host=EndpointBase.fxpractice_rest + FxHost.api_path,
        stream_host=EndpointBase.fxpractice_streaming + FxHost.api_path
    )
    fxLive: FxHost = FxHost(
        rest_host=EndpointBase.fxlive_rest + FxHost.api_path,
        stream_host=EndpointBase.fxlive_streaming + FxHost.api_path
    )
    
    def __eq__(self, obj) -> bool:
        return obj.__eq__(self.value)
    
    @property
    def rest_host(self):
        return self.value.rest_host
    
    @property
    def stream_host(self):
        return self.value.stream_host

__all__ = tuple(exporting(__name__, ...))
