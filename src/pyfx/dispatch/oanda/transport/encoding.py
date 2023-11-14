"""Async JSON Encoder support for API [Prototype]"""

from json import JSONEncoder
from typing import Any, AsyncIterator

from .transport_base import TransportType
from .data import ApiObject, TransportObject, JsonTypesRepository

from ..io.segment import AsyncSegmentChannel

class ApiJsonEncoder(JSONEncoder):
    """JSON encoder for API Object classes"""

    __slots__ = (
        ## slots from properties in Python JSONEncoder (Python 3.11)
        "item_separator", "key_separator", "skipkeys",  "ensure_ascii",
        "check_circular", "allow_nan", "sort_keys", "indent",
    )

    def __init__(self):
        super().__init__(ensure_ascii=False, check_circular=False)

    def default(self, pyobj: Any) -> Any:
        ocls = pyobj.__class__
        typ: TransportType = ocls if isinstance(ocls, TransportType) else JsonTypesRepository.get_transport_type(ocls)  # type: ignore
        rslt = typ.unparse_py(pyobj, self)
        return rslt

    async def aencode_bytes_channel(self, object, channel: AsyncSegmentChannel):
        ## encoder support => bytes
        txtyp: TransportObject = object.transport_type
        async for token in txtyp.aiter_token_bytes(object, channel, self):
            channel.feed(token)

    async def aencode_bytes(self, object: ApiObject):
        async with AsyncSegmentChannel(empty_sequence=b'') as channel:
            self.aencode_bytes_channel(object, channel)
            # return channel.read()
            return channel.join_queued(b'')

    async def aiterencode(self, pyobj: Any) -> AsyncIterator[str]:
        """Simple async dispatch for iterencode(pyobj)"""
        for out in self.iterencode(pyobj):
            yield out

    def encode_bytes(object):
        if isinstance(object, ApiObject):
            return object.transport_type.unparse_bytes(object)
        else:
            ## repository ...
            pass


__all__ = ("ApiJsonEncoder",)
