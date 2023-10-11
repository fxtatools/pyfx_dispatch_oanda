
"""MarketOrderReason definition for OANDA v20 REST API (3.0.25)"""

from enum import Enum


class MarketOrderReason(str, Enum):
    """
    The reason that the Market Order was created
    """

    CLIENT_ORDER = 'CLIENT_ORDER'
    TRADE_CLOSE = 'TRADE_CLOSE'
    POSITION_CLOSEOUT = 'POSITION_CLOSEOUT'
    MARGIN_CLOSEOUT = 'MARGIN_CLOSEOUT'
    DELAYED_TRADE_CLOSE = 'DELAYED_TRADE_CLOSE'


__all__ = ("MarketOrderReason",)
