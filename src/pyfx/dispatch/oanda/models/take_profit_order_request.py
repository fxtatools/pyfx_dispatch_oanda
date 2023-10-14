
"""TakeProfitOrderRequest model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal

from ..transport.transport_fields import TransportField

from .request_mixins import StopsRequestBase

from .order_type import OrderType
from .common_types import PriceValue
from .time_in_force import TimeInForce


class TakeProfitOrderRequest(StopsRequestBase):
    """
    A TakeProfitOrderRequest specifies the parameters that may be set when creating a Take Profit Order.
    """

    type: Annotated[Literal[OrderType.TAKE_PROFIT], TransportField(OrderType.TAKE_PROFIT)] = OrderType.TAKE_PROFIT
    """
    The type of the Order to Create. Must be set to \"TAKE_PROFIT\" when creating a Take Profit Order.
    """

    price: Annotated[PriceValue, TransportField(...)]
    """
    The price threshold specified for the TakeProfit Order. The associated Trade will be closed by a market price that is equal to or better than this threshold.
    """

    time_in_force: Annotated[TimeInForce, TransportField(TimeInForce.GTC, alias="timeInForce")]
    """
    The time-in-force requested for the TakeProfit Order. Restricted to \"GTC\", \"GFD\" and \"GTD\" for TakeProfit Orders.
    """

__all__ = ("TakeProfitOrderRequest",)
