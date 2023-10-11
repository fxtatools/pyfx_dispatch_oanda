"""TradeIdMixin definition"""

from typing import Optional

from ..transport import ApiObject, TransportField

from .common_types import ClientId, TradeId


class TradeIdMixin(ApiObject):
    """
    Mixin class for types representing a `trade_id` and `client_trade_id`
    """

    trade_id: TradeId = TransportField(None, alias="tradeID")
    """
    The ID of the Trade
    """

    client_trade_id: Optional[ClientId] = TransportField(None, alias="clientTradeID")
    """
    The client ID of the Trade
    """


__all__ = ("TradeIdMixin",)
