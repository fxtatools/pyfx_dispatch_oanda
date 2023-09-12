## Constants for HTTP requests

from enum import Enum

class RequestMethod(Enum):
    '''Enum class for HTTP request methods

For request methods `GET`, `HEAD`,  and `OPTIONS`, the 
`RequestMethod` instance method `isFormRequest()` returns
`False`. 

For `POST`, `PUT`, `PATCH`, and `DELETE` request methods, 
`isFormRequest()` returns `True`'''
    GET = 1
    HEAD = 1 << 2
    OPTIONS = 1 << 3
    _FORM_OFFSET = 1 << 4
    POST = 1 << _FORM_OFFSET + 1 | _FORM_OFFSET
    PUT = 1 << _FORM_OFFSET + 2 | _FORM_OFFSET
    PATCH = 1 << _FORM_OFFSET + 3 | _FORM_OFFSET
    DELETE = 1 << _FORM_OFFSET + 4 | _FORM_OFFSET

    def isFormRequest(self) -> bool:
        return (self.value & self.__class__._FORM_OFFSET.value) != 0
