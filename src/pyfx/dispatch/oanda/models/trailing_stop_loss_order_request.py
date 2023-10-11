
"""TrailingStopLossOrderRequest model definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal

from ..transport import TransportField

from .request_mixins import StopsRequestBase
from .common_types import PriceValue

from .order_type import OrderType
from .time_in_force import TimeInForce


class TrailingStopLossOrderRequest(StopsRequestBase):
    """
    A TrailingStopLossOrderRequest specifies the parameters that may be set when creating a Trailing Stop Loss Order.
    """

    type: Literal[OrderType.TRAILING_STOP_LOSS] = TransportField(OrderType.TRAILING_STOP_LOSS)
    """
    The type of the Order to Create. Must be set to \"TRAILING_STOP_LOSS\" when creating a Trailng Stop Loss Order.
    """

    distance: PriceValue = TransportField(...)
    """
    The price distance (in price units) specified for the TrailingStopLoss Order.
    """

    time_in_force: TimeInForce = TransportField(TimeInForce.GTC, alias="timeInForce")
    """
    The time-in-force requested for the TrailingStopLoss Order. Restricted to \"GTC\", \"GFD\" and \"GTD\" for TrailingStopLoss Orders.
    """


__all__ = ("TrailingStopLossOrderRequest",)
