## common definitions for response handling

from .util.naming import exporting

from .transport.data import ApiObject

from dataclasses import dataclass
from typing import Mapping, Optional


@dataclass
class ResponseInfo:
    ## intermediate dataclass for the generator-based response workflow
    response_types_map: Mapping[int, type[ApiObject]]
    status: int
    reason: str
    headers: Mapping[str, str]
    content_type: str
    content_encoding: Optional[str] = None


REST_CONTENT_TYPE_BYTES: bytes = b'application/json'
REST_CONTENT_TYPE: str = 'application/json'

STREAM_CONTENT_TYPE_BYTES: bytes=b'application/octet-stream'
STREAM_CONTENT_TYPE: str='application/octet-stream'

__all__ = tuple(exporting(__name__, ...))
