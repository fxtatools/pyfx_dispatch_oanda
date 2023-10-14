
"""model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal

from ..transport.transport_fields import TransportField

from .stop_order_transaction import StopOrderTransaction
from .transaction_mixins import RejectTxn
from .transaction_type import TransactionType


class StopOrderRejectTransaction(RejectTxn, StopOrderTransaction):
    """
    A StopOrderRejectTransaction represents the rejection of the creation of a Stop Order.
    """

    type: Annotated[Literal[TransactionType.STOP_ORDER_REJECT], TransportField(TransactionType.STOP_ORDER_REJECT)] = TransactionType.STOP_ORDER_REJECT
    """
    The Type of the Transaction. Always set to \"STOP_ORDER_REJECT\" in a StopOrderRejectTransaction.
    """


__all__ = ("StopOrderRejectTransaction",)
