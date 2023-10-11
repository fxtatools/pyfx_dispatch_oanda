
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Optional


from ..transport import ApiObject, TransportField
from ..util import exporting


class PositionBookBucket(ApiObject):
    """
    The position book data for a partition of the instrument's prices.
    """
    price: Optional[str] = TransportField(None)
    """
    The lowest price (inclusive) covered by the bucket. The bucket covers the price range from the price to price + the position book's bucketWidth.
    """
    long_count_percent: Optional[str] = TransportField(None, alias="longCountPercent")
    """
    The percentage of the total number of positions represented by the long positions found in this bucket.
    """
    short_count_percent: Optional[str] = TransportField(None, alias="shortCountPercent")
    """
    The percentage of the total number of positions represented by the short positions found in this bucket.
    """


__all__ = exporting(__name__, ...)
