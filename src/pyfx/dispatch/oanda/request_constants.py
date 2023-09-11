## Constants for HTTP requests

from enum import Enum

class RequestMethod(Enum):
    '''Enum class for HTTP request methods

For request methods `GET` and `HEAD`, the instance method
`isContentRequest()` returns `False`. For other request
methods, `isContentRequest()` returns `True`'''
    GET = 1
    HEAD = 2
    _CONTENT_OFFSET = HEAD << 1
    OPTIONS = 1 << _CONTENT_OFFSET | _CONTENT_OFFSET
    POST = 2 << _CONTENT_OFFSET | _CONTENT_OFFSET
    PUT = 3 << _CONTENT_OFFSET | _CONTENT_OFFSET
    PATCH = 4 << _CONTENT_OFFSET | _CONTENT_OFFSET
    DELETE = 5 << _CONTENT_OFFSET | _CONTENT_OFFSET

    def isContentRequest(self) -> bool:
        return (self.value & self.__class__._CONTENT_OFFSET.value) != 0
