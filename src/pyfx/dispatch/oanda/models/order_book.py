
"""model definition for OANDA v20 REST API (3.0.25)"""


from pandas import Timestamp


from typing import Annotated, Optional

from .order_book_bucket import OrderBookBucket


from ..transport import ApiObject, TransportField
from ..util import exporting


class OrderBook(ApiObject):
    """
    The representation of an instrument's order book at a point in time
    """
    instrument: Annotated[Optional[str], TransportField(None)]
    """
    The order book's instrument
    """
    time: Annotated[Timestamp, TransportField(None)]
    """
    The time when the order book snapshot was created.
    """
    price: Annotated[Optional[str], TransportField(None)]
    """
    The price (midpoint) for the order book's instrument at the time of the order book snapshot
    """
    bucket_width: Annotated[Optional[str], TransportField(None, alias="bucketWidth")]
    """
    The price width for each bucket. Each bucket covers the price range from the bucket's price to the bucket's price + bucketWidth.
    """
    buckets: Annotated[Optional[list[OrderBookBucket]], TransportField(None)]
    """
    The partitioned order book, divided into buckets using a default bucket width. These buckets are only provided for price ranges which actually contain order or position data.
    """


__all__ = exporting(__name__, ...)
