
"""TrailingStopLossOrderRejectTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal

from ..transport import TransportField

from .trailing_stop_loss_order_transaction import TrailingStopLossOrderTransaction
from .transaction_mixins import RejectTxn
from .transaction_type import TransactionType


class TrailingStopLossOrderRejectTransaction(RejectTxn, TrailingStopLossOrderTransaction):
    """
    A TrailingStopLossOrderRejectTransaction represents the rejection of the creation of a TrailingStopLoss Order.
    """

    type: Annotated[Literal[TransactionType.TRAILING_STOP_LOSS_ORDER_REJECT], TransportField(TransactionType.TRAILING_STOP_LOSS_ORDER_REJECT)] = TransactionType.TRAILING_STOP_LOSS_ORDER_REJECT
    """
    The Type of the Transaction. Always set to \"TRAILING_STOP_LOSS_ORDER_REJECT\" in a TrailingStopLossOrderRejectTransaction.
    """


__all__ = ("TrailingStopLossOrderRejectTransaction",)
