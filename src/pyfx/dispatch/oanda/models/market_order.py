
"""MarketOrder model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal, Optional

from ..transport import TransportField

from .order_mixins import UnitsOrderBase

from .common_types import PriceValue
from .order_type import OrderType
from .time_in_force import TimeInForce

from .market_order_delayed_trade_close import MarketOrderDelayedTradeClose
from .market_order_margin_closeout import MarketOrderMarginCloseout
from .market_order_position_closeout import MarketOrderPositionCloseout
from .market_order_trade_close import MarketOrderTradeClose


class MarketOrder(UnitsOrderBase):
    """
    A MarketOrder is an order that is filled immediately upon creation using the current market price.
    """

    type: Annotated[Literal[OrderType.MARKET], TransportField(OrderType.MARKET)] = OrderType.MARKET
    """
    The type of the Order. Always set to \"MARKET\" for Market Orders."""

    time_in_force: Annotated[TimeInForce, TransportField(TimeInForce.FOK, alias="timeInForce")]
    """
    The time-in-force requested for the Market Order. Restricted to FOK or IOC for a MarketOrder.
    """

    price_bound: Annotated[Optional[PriceValue], TransportField(None, alias="priceBound")]
    """
    The worst price that the client is willing to have the Market Order filled at.
    """

    trade_close: Annotated[Optional[MarketOrderTradeClose], TransportField(None, alias="tradeClose")]
    """
    Details of the Trade requested to be closed, only provided when the Market Order is being used to explicitly close a Trade.
    """

    long_position_closeout: Annotated[Optional[MarketOrderPositionCloseout], TransportField(None, alias="longPositionCloseout")]
    """
    Details of the long Position requested to be closed out, only provided when a Market Order is being used to explicitly closeout a long Position.
    """

    short_position_closeout: Annotated[Optional[MarketOrderPositionCloseout], TransportField(None, alias="shortPositionCloseout")]
    """
    Details of the short Position requested to be closed out, only provided when a Market Order is being used to explicitly closeout a short Position.
    """

    margin_closeout: Annotated[Optional[MarketOrderMarginCloseout], TransportField(None, alias="marginCloseout")]
    """
    Details of the Margin Closeout that this Market Order was created for
    """

    delayed_trade_close: Annotated[Optional[MarketOrderDelayedTradeClose], TransportField(None, alias="delayedTradeClose")]
    """
    Details of the delayed Trade close that this Market Order was created for
    """


__all__ = ("MarketOrder",)
