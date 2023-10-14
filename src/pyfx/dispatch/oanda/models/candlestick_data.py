
"""CandlestickData model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField

from .common_types import PriceValue


class CandlestickData(ApiObject):
    """
    The price data (open, high, low, close) for the Candlestick representation.
    """

    o: Annotated[PriceValue, TransportField(...)]
    """The first (open) price in the time-range represented by the candlestick.
    """

    h: Annotated[PriceValue, TransportField(...)]
    """The highest price in the time-range represented by the candlestick.
    """

    l: Annotated[PriceValue, TransportField(...)]
    """The lowest price in the time-range represented by the candlestick.
    """

    c: Annotated[PriceValue, TransportField(...)]
    """The last (closing) price in the time-range represented by the candlestick.
    """


__all__ = ("CandlestickData",)
