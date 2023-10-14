
"""model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal

from ..transport.transport_fields import TransportField

from .take_profit_order_transaction import TakeProfitOrderTransaction
from .transaction_mixins import RejectTxn
from .transaction_type import TransactionType


class TakeProfitOrderRejectTransaction(RejectTxn, TakeProfitOrderTransaction):
    """
    A TakeProfitOrderRejectTransaction represents the rejection of the creation of a TakeProfit Order.
    """

    type: Annotated[Literal[TransactionType.TAKE_PROFIT_ORDER_REJECT], TransportField(TransactionType.TAKE_PROFIT_ORDER_REJECT)] = TransactionType.TAKE_PROFIT_ORDER_REJECT
    """
    The Type of the Transaction. Always set to \"TAKE_PROFIT_ORDER_REJECT\" in a TakeProfitOrderRejectTransaction.
    """


__all__ = ("TakeProfitOrderRejectTransaction",)
