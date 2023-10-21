"""CancellableOrderType definition for OANDA v20 REST API (3.0.25)"""

from enum import Enum


class CancellableOrderType(str, Enum):
    """
    The type of the Order.
    """

    LIMIT = 'LIMIT'
    STOP = 'STOP'
    MARKET_IF_TOUCHED = 'MARKET_IF_TOUCHED'
    TAKE_PROFIT = 'TAKE_PROFIT'
    STOP_LOSS = 'STOP_LOSS'
    TRAILING_STOP_LOSS = 'TRAILING_STOP_LOSS'


__all__ = ("CancellableOrderType",)
