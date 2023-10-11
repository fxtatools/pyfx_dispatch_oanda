
"""MarketOrderRequest model definition for OANDA v20 REST API (3.0.25)"""

from .request_mixins import PriceBoundedRequest

from typing import Literal

from ..transport import TransportField

from .order_type import OrderType
from .time_in_force import TimeInForce


class MarketOrderRequest(PriceBoundedRequest):
    """
    A MarketOrderRequest specifies the parameters that may be set when creating a Market Order.
    """

    type: Literal[OrderType.MARKET] = TransportField(OrderType.MARKET)
    """
    The type of the Order to Create. Must be set to \"MARKET\" when creating a Market Order.
    """

    time_in_force: TimeInForce = TransportField(TimeInForce.FOK, alias="timeInForce")
    """
    The time-in-force requested for the Market Order. Restricted to FOK or
    IOC for a MarketOrder.
    """


__all__ = ("MarketOrderRequest",)
