"""LimitOrder model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal, Optional

from ..transport.transport_fields import TransportField

from .order_mixins import UnitsOrderBase
from .order_mixins import LimitOrderMixin

from .common_types import PriceValue
from .order_type import OrderType
from .time_in_force import TimeInForce

class LimitOrder(UnitsOrderBase, LimitOrderMixin):
    """
    A LimitOrder is an order that is created with a price threshold, and will only be filled by a price that is equal to or better than the threshold.
    """

    type: Annotated[Literal[OrderType.LIMIT], TransportField(OrderType.LIMIT)] = OrderType.LIMIT
    """
    The type of the Order. Always set to \"LIMIT\" for Limit Orders.
    """

    price: Annotated[Optional[PriceValue], TransportField(...)]
    """
    The price threshold specified for the Limit Order. The Limit Order will only be filled by a market price that is equal to or better than this price.
    """

    time_in_force: Annotated[Optional[TimeInForce], TransportField(TimeInForce.GTC, alias="timeInForce")]
    """
    The time-in-force requested for the Limit Order.
    """



__all__ = ("LimitOrder",)
