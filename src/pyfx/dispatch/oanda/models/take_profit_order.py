
"""TakeProfitOrder model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal

from ..transport import TransportField

from .order_mixins import LimitOrderMixin, ReplacesOrderMixin
from .trade_id_mixin import TradeIdMixin

from .common_types import PriceValue
from .order_type import OrderType
from .time_in_force import TimeInForce


class TakeProfitOrder(LimitOrderMixin, TradeIdMixin, ReplacesOrderMixin):
    """
    A TakeProfitOrder is an order that is linked to an open Trade and created with a price threshold. The Order will be filled (closing the Trade) by the first price that is equal to or better than the threshold. A TakeProfitOrder cannot be used to open a new Position.
    """

    type: Annotated[Literal[OrderType.TAKE_PROFIT], TransportField(OrderType.TAKE_PROFIT)] = OrderType.TAKE_PROFIT
    """
    The type of the Order. Always set to \"TAKE_PROFIT\" for Take Profit Orders.
    """

    price: Annotated[PriceValue, TransportField(...)]
    """
    The price threshold specified for the TakeProfit Order. The associated Trade will be closed by a market price that is equal to or better than this threshold.
    """

    time_in_force: Annotated[TimeInForce, TransportField(TimeInForce.GTC, alias="timeInForce")]
    """
    The time-in-force requested for the TakeProfit Order. Restricted to \"GTC\", \"GFD\" and \"GTD\" for TakeProfit Orders.
    """


__all__ = ("TakeProfitOrder",)
