"""TradeStateFilter definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum


class TradeStateFilter(ApiEnum):
    """
    The state to filter the Trades by
    """

    __finalize__: ClassVar[Literal[True]] = True

    OPEN = 'OPEN'
    """The Trades that are currently open"""

    CLOSED = 'CLOSED'
    """The Trades that have been fully closed"""

    CLOSE_WHEN_TRADEABLE = 'CLOSE_WHEN_TRADEABLE'
    """The Trades that will be closed as soon as the trades' instrument becomes tradeable"""

    ALL = 'ALL'
    """The Trades that are in any of the possible states."""


__all__ = ("TradeStateFilter",)
