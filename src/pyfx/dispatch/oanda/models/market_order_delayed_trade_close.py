"""MarketOrderDelayedTradeClose model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField

from .common_types import TradeId, ClientId, TransactionId


class MarketOrderDelayedTradeClose(ApiObject):
    """
    Details for the Market Order extensions specific to a Market Order placed with the intent of fully closing a specific open trade that should have already been closed but wasn't due to halted market conditions
    """

    trade_id: Annotated[TradeId, TransportField(..., alias="tradeID")]
    """
    The ID of the Trade being closed
    """

    client_trade_id: Annotated[Optional[ClientId], TransportField(None, alias="clientTradeID")]
    """
    The Client ID of the Trade being closed
    """

    source_transaction_id: Annotated[TransactionId, TransportField(..., alias="sourceTransactionID")]
    """
    The Transaction ID of the DelayedTradeClosure transaction to which this Delayed Trade Close belongs to
    """


__all__ = ("MarketOrderDelayedTradeClose",)
