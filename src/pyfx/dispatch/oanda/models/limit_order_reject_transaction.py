
"""LimitOrderRejectTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal

from ..transport import TransportField

from .limit_order_transaction import LimitOrderTransaction
from .transaction_mixins import RejectTxn
from .transaction_type import TransactionType


class LimitOrderRejectTransaction(RejectTxn, LimitOrderTransaction):
    """
    A LimitOrderRejectTransaction represents the rejection of the creation of a Limit Order.
    """

    type: Literal[TransactionType.LIMIT_ORDER_REJECT] = TransportField(TransactionType.LIMIT_ORDER_REJECT)
    """
    The Type of the Transaction. Always set to \"LIMIT_ORDER_REJECT\" in a LimitOrderRejectTransaction.
    """


__all__ = ("LimitOrderRejectTransaction",)
