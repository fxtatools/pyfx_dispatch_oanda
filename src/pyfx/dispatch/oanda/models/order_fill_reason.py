"""OrderFillReason definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum


class OrderFillReason(ApiEnum):
    """
    The reason that an Order was filled
    """


    __finalize__: ClassVar[Literal[True]] = True

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


__all__ = ("OrderFillReason",)
