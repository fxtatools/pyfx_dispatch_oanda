
"""TrailingStopLossOrderTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal

from ..transport import TransportField

from .transaction_mixins import OrderDistanceStopsTransaction
from .transaction_type import TransactionType
from .time_in_force import TimeInForce
from .trailing_stop_loss_order_reason import TrailingStopLossOrderReason


class TrailingStopLossOrderTransaction(OrderDistanceStopsTransaction):
    """
    A TrailingStopLossOrderTransaction represents the creation of a TrailingStopLoss Order in the user's Account.
    """

    type: Literal[TransactionType.TRAILING_STOP_LOSS_ORDER] = TransportField(TransactionType.TRAILING_STOP_LOSS_ORDER)
    """
    The Type of the Transaction. Always set to \"TRAILING_STOP_LOSS_ORDER\" in a TrailingStopLossOrderTransaction.
    """

    time_in_force: TimeInForce = TransportField(TimeInForce.GTC, alias="timeInForce")
    """
    The time-in-force requested for the TrailingStopLoss Order. Restricted to \"GTC\", \"GFD\" and \"GTD\" for TrailingStopLoss Orders.
    """

    reason: TrailingStopLossOrderReason = TransportField(...)
    """
    The reason that the Trailing Stop Loss Order was initiated
    """


__all__ = ("TrailingStopLossOrderTransaction",)
