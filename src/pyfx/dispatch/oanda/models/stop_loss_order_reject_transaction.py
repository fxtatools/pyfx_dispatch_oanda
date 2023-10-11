
"""StopLossOrderRejectTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal

from ..transport import TransportField

from .stop_loss_order_transaction import StopLossOrderTransaction
from .transaction_mixins import RejectTxn
from .transaction_type import TransactionType


class StopLossOrderRejectTransaction(RejectTxn, StopLossOrderTransaction):
    """
    A StopLossOrderRejectTransaction represents the rejection of the creation of a StopLoss Order.
    """

    type: Literal[TransactionType.STOP_LOSS_ORDER_REJECT] = TransportField(TransactionType.STOP_LOSS_ORDER_REJECT)
    """
    The Type of the Transaction. Always set to \"STOP_LOSS_ORDER_REJECT\" in a StopLossOrderRejectTransaction.
    """


__all__ = ("StopLossOrderRejectTransaction",)
