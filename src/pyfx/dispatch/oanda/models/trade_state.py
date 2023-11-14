"""TradeState definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum


class TradeState(ApiEnum):
    """
    The current state of the Trade, one of OPEN, CLOSED, or CLOSE_WHEN_TRADEABLE
    """


    __finalize__: ClassVar[Literal[True]] = True

    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    CLOSE_WHEN_TRADEABLE = 'CLOSE_WHEN_TRADEABLE'


__all__ = ("TradeState",)
