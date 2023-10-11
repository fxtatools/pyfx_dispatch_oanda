"""OrderCancelRejectTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal

from ..transport import TransportField

from .order_cancel_transaction import OrderCancelTransaction
from .transaction_mixins import RejectTxn
from .transaction_type import TransactionType

class OrderCancelRejectTransaction(RejectTxn, OrderCancelTransaction):
    """
    An OrderCancelRejectTransaction represents the rejection of the cancellation of an Order in the client's Account.
    """

    type: Literal[TransactionType.ORDER_CANCEL_REJECT] = TransportField(TransactionType.ORDER_CANCEL_REJECT)
    """
    The Type of the Transaction. Always set to \"ORDER_CANCEL_REJECT\" for an OrderCancelRejectTransaction.
    """


__all__ = ("OrderCancelRejectTransaction",)
