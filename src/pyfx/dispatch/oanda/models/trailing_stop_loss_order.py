
"""TrailingStopLossOrder model definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal, Optional

from ..transport import TransportField

from .order_mixins import LimitOrderMixin, ReplacesOrderMixin
from .trade_id_mixin import TradeIdMixin
from .order_type import OrderType
from .common_types import PriceValue
from .order_mixins import UnitsOrderBase
from .time_in_force import TimeInForce


class TrailingStopLossOrder(UnitsOrderBase, LimitOrderMixin, TradeIdMixin, ReplacesOrderMixin):
    """
    A TrailingStopLossOrder is an order that is linked to an open Trade and created with a price distance. The price distance is used to calculate a trailing stop value for the order that is in the losing direction from the market price at the time of the order's creation. The trailing stop value will follow the market price as it moves in the winning direction, and the order will filled (closing the Trade) by the first price that is equal to or worse than the trailing stop value. A TrailingStopLossOrder cannot be used to open a new Position.
    """

    type: Literal[OrderType.TRAILING_STOP_LOSS] = TransportField(OrderType.TRAILING_STOP_LOSS)
    """
    The type of the Order. Always set to "TRAILING_STOP_LOSS" for Trailing Stop Loss Orders.
    """

    distance: PriceValue = TransportField(...)
    """
    The price distance (in price units) specified for the TrailingStopLoss Order.
    """

    time_in_force: TimeInForce = TransportField(TimeInForce.GTC, alias="timeInForce")
    """
    The time-in-force requested for the TrailingStopLoss Order. Restricted to \"GTC\", \"GFD\" and \"GTD\" for TrailingStopLoss Orders.
    """

    trailing_stop_value: Optional[PriceValue] = TransportField(None, alias="trailingStopValue")
    """
    The trigger price for the Trailing Stop Loss Order. The trailing stop value will trail (follow) the market price by the TSL order's configured \"distance\" as the market price moves in the winning direction. If the market price moves to a level that is equal to or worse than the trailing stop value, the order will be filled and the Trade will be closed.
    """


__all__ = ("TrailingStopLossOrder",)
