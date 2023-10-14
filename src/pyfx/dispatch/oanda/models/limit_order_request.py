
"""model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal

from ..transport import TransportField

from .request_mixins import StopsRequestBase

from .common_types import PriceValue
from .order_type import OrderType
from .time_in_force import TimeInForce


class LimitOrderRequest(StopsRequestBase):
    """
    A LimitOrderRequest specifies the parameters that may be set when creating a Limit Order.
    """

    type: Annotated[Literal[OrderType.LIMIT], TransportField(OrderType.LIMIT)] = OrderType.LIMIT
    """
    The type of the Order to Create. Must be set to \"LIMIT\" when creating a Market Order.
    """

    price: Annotated[PriceValue, TransportField(...)]
    """
    The price threshold specified for the Limit Order. The Limit Order will only be filled by a market price that is equal to or better than this price.
    """

    time_in_force: Annotated[TimeInForce, TransportField(TimeInForce.GTC, alias="timeInForce")]
    """
    The time-in-force requested for the Limit Order.
    """


__all__ = ("LimitOrderRequest",)
