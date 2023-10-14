"""TradeIdMixin definition"""

from typing import Annotated, Optional

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField

from .common_types import ClientId, TradeId


class TradeIdMixin(ApiObject):
    """
    Mixin class for types representing a `trade_id` and `client_trade_id`
    """

    trade_id: Annotated[TradeId, TransportField(None, alias="tradeID")]
    """
    The ID of the Trade
    """

    client_trade_id: Annotated[Optional[ClientId], TransportField(None, alias="clientTradeID")]
    """
    The client ID of the Trade
    """


__all__ = ("TradeIdMixin",)
