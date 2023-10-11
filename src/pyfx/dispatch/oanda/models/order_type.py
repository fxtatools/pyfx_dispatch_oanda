
"""OrderType definition for OANDA v20 REST API (3.0.25) and subsequent"""

from enum import Enum


class OrderType(str, Enum):
    """
    The type of the Order.
    """

    MARKET = 'MARKET'
    """Market Order"""

    LIMIT = 'LIMIT'
    """Limit Order"""

    STOP = 'STOP'
    """Stop Order"""

    MARKET_IF_TOUCHED = 'MARKET_IF_TOUCHED'
    """Market-if-touched Order"""

    TAKE_PROFIT = 'TAKE_PROFIT'
    """Take Profit Order"""

    STOP_LOSS = 'STOP_LOSS'
    """Stop Loss Order"""

    GUARANTEED_STOP_LOSS = 'GUARANTEED_STOP_LOSS'
    """
    Guaranteed Stop Loss Order

    Supplemental to the fxTrade v20 API version 3.0.25
    """

    TRAILING_STOP_LOSS = 'TRAILING_STOP_LOSS'
    """Trailing Stop Loss Order"""

    FIXED_PRICE = 'FIXED_PRICE'
    """Fixed Price Order"""


__all__ = ("OrderType",)
