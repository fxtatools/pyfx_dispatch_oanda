
"""MarketIfTouchedOrderRequest model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal

from ..transport.transport_fields import TransportField

from .request_mixins import PriceBoundedRequest, StopsRequestBase
from .common_types import PriceValue
from .order_type import OrderType
from .time_in_force import TimeInForce


class MarketIfTouchedOrderRequest(PriceBoundedRequest, StopsRequestBase):
    """
    A MarketIfTouchedOrderRequest specifies the parameters that may be set when creating a Market-if-Touched Order.
    """

    type: Annotated[Literal[OrderType.MARKET_IF_TOUCHED], TransportField(OrderType.MARKET_IF_TOUCHED)] = OrderType.MARKET_IF_TOUCHED
    """
    The type of the Order to Create. Must be set to \"MARKET_IF_TOUCHED\" when creating a Market If Touched Order.
    """

    price: Annotated[PriceValue, TransportField(...)]
    """
    The price threshold specified for the MarketIfTouched Order. The MarketIfTouched Order will only be filled by a market price that crosses this price from the direction of the market price at the time when the Order was created (the initialMarketPrice). Depending on the value of the Order's price and initialMarketPrice, the MarketIfTouchedOrder will behave like a Limit or a Stop Order.
    """

    time_in_force: Annotated[TimeInForce, TransportField(TimeInForce.GTC, alias="timeInForce")]
    """
    The time-in-force requested for the MarketIfTouched Order. Restricted to \"GTC\", \"GFD\" and \"GTD\" for MarketIfTouched Orders.
    """


__all__ = ("MarketIfTouchedOrderRequest",)
