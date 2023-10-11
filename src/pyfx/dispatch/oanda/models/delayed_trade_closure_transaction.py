
"""DelayedTradeClosureTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal, Optional

from ..transport import TransportField

from .transaction import Transaction
from .transaction_type import TransactionType
from .market_order_reason import MarketOrderReason
from .common_types import TradeId


class DelayedTradeClosureTransaction(Transaction):
    """
    A DelayedTradeClosure Transaction is created administratively to indicate open trades that should have been closed but weren't because the open trades' instruments were untradeable at the time. Open trades listed in this transaction will be closed once their respective instruments become tradeable.
    """

    type: Literal[TransactionType.DELAYED_TRADE_CLOSURE] = TransportField(TransactionType.DELAYED_TRADE_CLOSURE)
    """
    The Type of the Transaction. Always set to \"DELAYED_TRADE_CLOSURE\" for an DelayedTradeClosureTransaction.
    """

    reason: Optional[MarketOrderReason] = TransportField(None)
    """
    The reason for the delayed trade closure
    """

    trade_ids: Optional[TradeId] = TransportField(None, alias="tradeIDs")
    ## TBD neither the OpenAPI specification nor the hub docs have specified a list/JSON array here
    """
    list of Trade ID's identifying the open trades that will be closed when their respective instruments become tradeable
    """


__all__ = ("DelayedTradeClosureTransaction",)
