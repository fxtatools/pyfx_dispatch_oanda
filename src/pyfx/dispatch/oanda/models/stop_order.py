
"""StopOrder model definition for OANDA v20 REST API (3.0.25)"""


from typing import Literal, Optional

from ..transport import TransportField

from .order_mixins import UnitsOrderBase
from .order_mixins import ReplacesOrderMixin
from .order_mixins import LimitOrderMixin
from .common_types import PriceValue
from .order_type import OrderType
from .time_in_force import TimeInForce


class StopOrder(UnitsOrderBase, LimitOrderMixin, ReplacesOrderMixin):
    """
    A StopOrder is an order that is created with a price threshold, and will only be filled by a price that is equal to or worse than the threshold.
    """

    type: Literal[OrderType.STOP] = TransportField(OrderType.STOP)
    """
    The type of the Order. Always set to \"STOP\" for Stop Orders.
    """

    price: PriceValue = TransportField(...)
    """
    The price threshold specified for the Stop Order. The Stop Order will only be filled by a market price that is equal to or worse than this price.
    """

    price_bound: Optional[PriceValue] = TransportField(None, alias="priceBound")
    """
    The worst market price that may be used to fill this Stop Order. If the market gaps and crosses through both the price and the priceBound, the Stop Order will be cancelled instead of being filled.
    """

    time_in_force: TimeInForce = TransportField(TimeInForce.GTC, alias="timeInForce")
    """
    The time-in-force requested for the Stop Order.
    """


__all__ = ("StopOrder",)
