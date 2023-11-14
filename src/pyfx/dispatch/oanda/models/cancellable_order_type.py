"""CancellableOrderType definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum


class CancellableOrderType(ApiEnum):
    """
    The type of the Order.
    """


    __finalize__: ClassVar[Literal[True]] = True

    LIMIT = 'LIMIT'
    STOP = 'STOP'
    MARKET_IF_TOUCHED = 'MARKET_IF_TOUCHED'
    TAKE_PROFIT = 'TAKE_PROFIT'
    STOP_LOSS = 'STOP_LOSS'
    TRAILING_STOP_LOSS = 'TRAILING_STOP_LOSS'


__all__ = ("CancellableOrderType",)
