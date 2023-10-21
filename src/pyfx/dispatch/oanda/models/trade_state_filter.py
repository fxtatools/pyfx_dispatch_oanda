"""TradeStateFilter definition for OANDA v20 REST API (3.0.25)"""

from enum import Enum


class TradeStateFilter(str, Enum):
    """
    The state to filter the Trades by
    """

    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    CLOSE_WHEN_TRADEABLE = 'CLOSE_WHEN_TRADEABLE'
    ALL = 'ALL'


__all__ = ("TradeStateFilter",)
