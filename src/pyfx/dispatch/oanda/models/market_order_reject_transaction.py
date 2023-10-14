
"""model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal

from ..transport import TransportField

from .market_order_transaction import MarketOrderTransaction
from .transaction_mixins import RejectTxn
from .transaction_type import TransactionType


class MarketOrderRejectTransaction(RejectTxn, MarketOrderTransaction):
    """
    A MarketOrderRejectTransaction represents the rejection of the creation of a Market Order.
    """

    type: Annotated[Literal[TransactionType.MARKET_ORDER_REJECT], TransportField(TransactionType.MARKET_ORDER_REJECT)] = TransactionType.MARKET_ORDER_REJECT
    """
    The Type of the Transaction. Always set to \"MARKET_ORDER_REJECT\" in a MarketOrderRejectTransaction.
    """


__all__ = ("MarketOrderRejectTransaction",)
