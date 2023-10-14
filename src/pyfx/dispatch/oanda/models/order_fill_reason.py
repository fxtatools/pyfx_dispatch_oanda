
"""model definition for OANDA v20 REST API (3.0.25)"""


from enum import Enum


from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting


class OrderFillReason(str, Enum):
    """
    The reason that an Order was filled
    """

    """
    allowed enum values
    """
    LIMIT_ORDER = 'LIMIT_ORDER'
    STOP_ORDER = 'STOP_ORDER'
    MARKET_IF_TOUCHED_ORDER = 'MARKET_IF_TOUCHED_ORDER'
    TAKE_PROFIT_ORDER = 'TAKE_PROFIT_ORDER'
    STOP_LOSS_ORDER = 'STOP_LOSS_ORDER'
    TRAILING_STOP_LOSS_ORDER = 'TRAILING_STOP_LOSS_ORDER'
    MARKET_ORDER = 'MARKET_ORDER'
    MARKET_ORDER_TRADE_CLOSE = 'MARKET_ORDER_TRADE_CLOSE'
    MARKET_ORDER_POSITION_CLOSEOUT = 'MARKET_ORDER_POSITION_CLOSEOUT'
    MARKET_ORDER_MARGIN_CLOSEOUT = 'MARKET_ORDER_MARGIN_CLOSEOUT'
    MARKET_ORDER_DELAYED_TRADE_CLOSE = 'MARKET_ORDER_DELAYED_TRADE_CLOSE'


__all__ = exporting(__name__, ...)
