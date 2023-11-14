"""Type definitions for StreamingPriceObject

See also:
- the `streaming_price_map` module, within this module's containing namespace
"""

from abc import ABC
from typing import Annotated, Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum
from ..transport.data import AbstractApiObject
from ..transport.transport_fields import TransportField


class StreamingPriceType(ApiEnum):

    __finalize__: ClassVar[Literal[True]] = True

    PRICE = "PRICE"
    HEARTBEAT = "HEARTBEAT"


class StreamingPriceObject(AbstractApiObject, ABC,
                           designator_key="type",
                           designator_type=StreamingPriceType):
    """Abstract base class for ClientPrice, PricingHeartbeat"""

    type:  Annotated[StreamingPriceType, TransportField(...)]
    """Designator field for implementation classes"""


__all__ = "StreamingPriceType", "StreamingPriceObject"
