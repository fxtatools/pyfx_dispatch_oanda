"""OrderBookBucket model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from .common_types import PriceValue, FloatValue


class OrderBookBucket(ApiObject):
    """
    The order book data for a partition of the instrument's prices.
    """

    price: Annotated[PriceValue, TransportField(...)]
    """
    The lowest price (inclusive) covered by the bucket. The bucket covers the price range from the price to price + the order book's bucketWidth.
    """

    long_count_percent: Annotated[FloatValue, TransportField(..., alias="longCountPercent")]
    """
    The percentage of the total number of orders represented by the long orders found in this bucket.
    """

    short_count_percent: Annotated[FloatValue, TransportField(..., alias="shortCountPercent")]
    """
    The percentage of the total number of orders represented by the short orders found in this bucket.
    """


__all__ = ("OrderBookBucket",)
