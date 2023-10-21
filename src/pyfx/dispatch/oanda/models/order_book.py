"""OrderBook model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField

from .common_types import InstrumentName, Time, PriceValue
from .order_book_bucket import OrderBookBucket


class OrderBook(ApiObject):
    """The representation of an instrument's order book at a point in time
    """

    instrument: Annotated[InstrumentName, TransportField(...)]
    """The order book's instrument
    """

    time: Annotated[Time, TransportField(...)]
    """The time when the order book snapshot was created.
    """

    price: Annotated[PriceValue, TransportField(...)]
    """The price (midpoint) for the order book's instrument at the time of the order book snapshot
    """

    bucket_width: Annotated[PriceValue, TransportField(..., alias="bucketWidth")]
    """The price width for each bucket. Each bucket covers the price range from the bucket's price to the bucket's price + bucketWidth.
    """

    buckets: Annotated[Optional[list[OrderBookBucket]], TransportField(None)]
    """The partitioned order book, divided into buckets using a default bucket width.

    These buckets are only provided for price ranges which actually contain order or position data.
    """


__all__ = ("OrderBook",)
