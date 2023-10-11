
"""PriceBucket model definition for OANDA v20 REST API (3.0.25)"""

from typing import Optional


from ..transport import ApiObject, TransportField
from .common_types import PriceValue, FloatValue


class PriceBucket(ApiObject):
    """
    A Price Bucket represents a price available for an amount of liquidity
    """

    price: PriceValue = TransportField(...)
    """
    The Price offered by the PriceBucket
    """

    liquidity: FloatValue = TransportField(...)
    """
    The amount of liquidity offered by the PriceBucket
    """


__all__ = ("PriceBucket",)
