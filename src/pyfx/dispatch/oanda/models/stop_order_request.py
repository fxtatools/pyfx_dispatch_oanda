
"""StopOrderRequest model definition for OANDA v20 REST API (3.0.25)"""


from typing import Annotated, Literal

from ..transport import TransportField

from .request_mixins import PriceBoundedRequest, StopsRequestBase
from .order_type import OrderType
from .common_types import PriceValue
from .time_in_force import TimeInForce


class StopOrderRequest(PriceBoundedRequest, StopsRequestBase):
    """
    A StopOrderRequest specifies the parameters that may be set when creating a Stop Order.
    """

    type: Annotated[Literal[OrderType.STOP], TransportField(OrderType.STOP)] = OrderType.STOP
    """
    The type of the Order to Create. Must be set to \"STOP\" when creating a Stop Order.
    """

    price: Annotated[PriceValue, TransportField(...)]
    """
    The price threshold specified for the Stop Order. The Stop Order will only be filled by a market price that is equal to or worse than this price.
    """

    time_in_force: Annotated[TimeInForce, TransportField(TimeInForce.GTC, alias="timeInForce")]
    """
    The time-in-force requested for the Stop Order.
    """


__all__ = ("StopOrderRequest",)
