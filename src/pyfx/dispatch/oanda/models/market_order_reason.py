
"""MarketOrderReason definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum


class MarketOrderReason(ApiEnum):
    """
    The reason that the Market Order was created
    """


    __finalize__: ClassVar[Literal[True]] = True

    CLIENT_ORDER = 'CLIENT_ORDER'
    TRADE_CLOSE = 'TRADE_CLOSE'
    POSITION_CLOSEOUT = 'POSITION_CLOSEOUT'
    MARGIN_CLOSEOUT = 'MARGIN_CLOSEOUT'
    DELAYED_TRADE_CLOSE = 'DELAYED_TRADE_CLOSE'


__all__ = ("MarketOrderReason",)
