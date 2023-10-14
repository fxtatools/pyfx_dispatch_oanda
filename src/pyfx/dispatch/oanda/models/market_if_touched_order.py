"""MarketIfTouchedOrder model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal, Optional

from .order_mixins import LimitOrderMixin
from .order_mixins import ReplacesOrderMixin

from ..transport.transport_fields import TransportField
from .order_type import OrderType
from .common_types import PriceValue
from .time_in_force import TimeInForce
from .market_if_touched_order_reason import MarketIfTouchedOrderReason


class MarketIfTouchedOrder(LimitOrderMixin, ReplacesOrderMixin):
    """
    A MarketIfTouchedOrder is an order that is created with a price threshold, and will only be filled by a market price that is touches or crosses the threshold.
    """

    type: Annotated[Literal[OrderType.MARKET_IF_TOUCHED], TransportField(OrderType.MARKET_IF_TOUCHED)] = OrderType.MARKET_IF_TOUCHED
    """
    The type of the Order. Always set to \"MARKET_IF_TOUCHED\" for Market If Touched Orders.
    """

    price: Annotated[PriceValue, TransportField(...)]
    """
    The price threshold specified for the MarketIfTouched Order. The MarketIfTouched Order will only be filled by a market price that crosses this price from the direction of the market price at the time when the Order was created (the initialMarketPrice). Depending on the value of the Order's price and initialMarketPrice, the MarketIfTouchedOrder will behave like a Limit or a Stop Order.
    """

    price_bound: Annotated[Optional[PriceValue], TransportField(None, alias="priceBound")]
    """
    The worst market price that may be used to fill this MarketIfTouched Order.
    """

    time_in_force: Annotated[TimeInForce, TransportField(TimeInForce.GTC, alias="timeInForce")]
    """
    The time-in-force requested for the MarketIfTouched Order. Restricted to \"GTC\", \"GFD\" and \"GTD\" for MarketIfTouched Orders.
    """

    initial_market_price: Annotated[Optional[PriceValue], TransportField(None, alias="initialMarketPrice")]
    """
    The Market price at the time when the MarketIfTouched Order was created.
    """

    reason: Annotated[MarketIfTouchedOrderReason, TransportField(...)]
    """
    The reason that the Market-if-touched order was initiated
    """


__all__ = ("MarketIfTouchedOrder",)
