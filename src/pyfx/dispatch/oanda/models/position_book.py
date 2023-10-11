
"""model definition for OANDA v20 REST API (3.0.25)"""


from pandas import Timestamp


from typing import Optional

from .position_book_bucket import PositionBookBucket


from ..transport import ApiObject, TransportField
from ..util import exporting


class PositionBook(ApiObject):
    """
    The representation of an instrument's position book at a point in time
    """
    instrument: Optional[str] = TransportField(None)
    """
    The position book's instrument
    """
    time: Timestamp = TransportField(None)
    """
    The time when the position book snapshot was created
    """
    price: Optional[str] = TransportField(None)
    """
    The price (midpoint) for the position book's instrument at the time of the position book snapshot
    """
    bucket_width: Optional[str] = TransportField(None, alias="bucketWidth")
    """
    The price width for each bucket. Each bucket covers the price range from the bucket's price to the bucket's price + bucketWidth.
    """
    buckets: Optional[list[PositionBookBucket]] = TransportField(None)
    """
    The partitioned position book, divided into buckets using a default bucket width. These buckets are only provided for price ranges which actually contain order or position data.
    """


__all__ = exporting(__name__, ...)
