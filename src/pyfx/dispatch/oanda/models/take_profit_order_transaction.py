
"""TakeProfitOrderTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal

from ..transport import TransportField

from .transaction_mixins import OrderStopsTransaction
from .transaction_type import TransactionType
from .common_types import PriceValue
from .time_in_force import TimeInForce
from .take_profit_order_reason import TakeProfitOrderReason

class TakeProfitOrderTransaction(OrderStopsTransaction):
    """
    A TakeProfitOrderTransaction represents the creation of a TakeProfit Order in the user's Account.
    """

    type: Literal[TransactionType.TAKE_PROFIT_ORDER] = TransportField(TransactionType.TAKE_PROFIT_ORDER)
    """
    The Type of the Transaction. Always set to \"TAKE_PROFIT_ORDER\" in a TakeProfitOrderTransaction.
    """

    price: PriceValue = TransportField(...)
    """
    The price threshold specified for the TakeProfit Order. The associated Trade will be closed by a market price that is equal to or better than this threshold.
    """

    time_in_force: TimeInForce = TransportField(TimeInForce.GTC, alias="timeInForce")
    """
    The time-in-force requested for the TakeProfit Order. Restricted to \"GTC\", \"GFD\" and \"GTD\" for TakeProfit Orders.
    """

    reason: TakeProfitOrderReason = TransportField(...)
    """
    The reason that the Take Profit Order was initiated
    """


__all__ = ("TakeProfitOrderTransaction",)
