
"""AccountChanges model definition for OANDA v20 REST API (3.0.25)"""

from typing import Optional

from .order import Order
from .position import Position
from .trade_summary import TradeSummary
from .transaction import Transaction

from ..transport import ApiObject, TransportField


class AccountChanges(ApiObject):
    """
    An AccountChanges Object is used to represent the changes to an Account's Orders, Trades and Positions since a specified Account TransactionID in the past.
    """

    orders_created: Optional[list[Order]] = TransportField(None, alias="ordersCreated")
    """
    The Orders created. These Orders may have been filled, cancelled or triggered in the same period.
    """

    orders_cancelled: Optional[list[Order]] = TransportField(None, alias="ordersCancelled")
    """The Orders cancelled."""

    orders_filled: Optional[list[Order]] = TransportField(None, alias="ordersFilled")
    """The Orders filled."""

    orders_triggered: Optional[list[Order]] = TransportField(None, alias="ordersTriggered")
    """The Orders triggered."""

    trades_opened: Optional[list[TradeSummary]] = TransportField(None, alias="tradesOpened")
    """The Trades opened."""

    trades_reduced: Optional[list[TradeSummary]] = TransportField(None, alias="tradesReduced")
    """The Trades reduced."""

    trades_closed: Optional[list[TradeSummary]] = TransportField(None, alias="tradesClosed")
    """The Trades closed."""

    positions: Optional[list[Position]] = TransportField(None)
    """The Positions changed."""

    transactions: Optional[list[Transaction]] = TransportField(None)
    """The Transactions that have been generated."""


__all__ = ("AccountChanges",)
