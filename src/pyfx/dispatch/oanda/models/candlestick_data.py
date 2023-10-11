
"""CandlestickData model definition for OANDA v20 REST API (3.0.25)"""

from ..transport import ApiObject, TransportField

from .common_types import PriceValue


class CandlestickData(ApiObject):
    """
    The price data (open, high, low, close) for the Candlestick representation.
    """

    o: PriceValue = TransportField(...)
    """The first (open) price in the time-range represented by the candlestick.
    """

    h: PriceValue = TransportField(...)
    """The highest price in the time-range represented by the candlestick.
    """

    l: PriceValue = TransportField(...)
    """The lowest price in the time-range represented by the candlestick.
    """

    c: PriceValue = TransportField(...)
    """The last (closing) price in the time-range represented by the candlestick.
    """


__all__ = ("CandlestickData",)
