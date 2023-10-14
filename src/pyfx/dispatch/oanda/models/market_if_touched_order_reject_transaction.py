
"""MarketIfTouchedOrderRejectTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal

from ..transport import TransportField

from .market_if_touched_order_transaction import MarketIfTouchedOrderTransaction
from .transaction_mixins import RejectTxn
from .transaction_type import TransactionType


class MarketIfTouchedOrderRejectTransaction(RejectTxn, MarketIfTouchedOrderTransaction):
    """
    A MarketIfTouchedOrderRejectTransaction represents the rejection of the creation of a MarketIfTouched Order.
    """
    type: Annotated[Literal[TransactionType.MARKET_IF_TOUCHED_ORDER_REJECT], TransportField(TransactionType.MARKET_IF_TOUCHED_ORDER_REJECT)] = TransactionType.MARKET_IF_TOUCHED_ORDER_REJECT
    """
    The Type of the Transaction. Always set to \"MARKET_IF_TOUCHED_ORDER_REJECT\" in a MarketIfTouchedOrderRejectTransaction.
    """


__all__ = ("MarketIfTouchedOrderRejectTransaction",)
