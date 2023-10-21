"""MarketOrderTradeClose model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from .common_types import FloatValue, TradeId, ClientId
from .transport_types import TransportDecmialAll


class MarketOrderTradeClose(ApiObject):
    """
    A MarketOrderTradeClose specifies the extensions to a Market Order that has been created specifically to close a Trade.
    """

    trade_id: Annotated[Optional[TradeId], TransportField(None, alias="tradeID")]
    """
    The ID of the Trade requested to be closed
    """

    client_trade_id: Annotated[Optional[ClientId], TransportField(None, alias="clientTradeID")]
    """
    The client ID of the Trade requested to be closed
    """

    units: Annotated[Optional[FloatValue], TransportField(None, transport_type=TransportDecmialAll)]
    """
    Indication of how much of the Trade to close. Either \"ALL\", or a DecimalNumber reflecting a partial close of the Trade.
    """


__all__ = ("MarketOrderTradeClose",)
