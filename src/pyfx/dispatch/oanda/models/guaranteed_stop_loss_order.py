"""Model definition for GuaranteedStopLossOrder, supplemental to v20 API 3.0.25"""

from typing import Annotated, Literal, Optional

from ..transport.transport_fields import TransportField

from .trade_id_mixin import TradeIdMixin
from .order_mixins import ReplacesOrderMixin
from .order_mixins import LimitOrderMixin
from .order_type import OrderType
from .common_types import PriceValue
from .time_in_force import TimeInForce


class GuaranteedStopLossOrder(TradeIdMixin, LimitOrderMixin, ReplacesOrderMixin):
    """
    A GuaranteedStopLossOrder is an order that is linked to an open Trade and created with a price threshold which is guaranteed against slippage that may occur as the market crosses the price set for that order. The Order will be filled (closing the Trade) by the first price that is equal to or worse than the threshold. The price level specified for the GuaranteedStopLossOrder must be at least the configured minimum distance (in price units) away from the entry price for the traded instrument. A GuaranteedStopLossOrder cannot be used to open a new Position.
    """

    type: Annotated[Literal[OrderType.GUARANTEED_STOP_LOSS], TransportField(OrderType.GUARANTEED_STOP_LOSS)] = OrderType.GUARANTEED_STOP_LOSS
    """
    The type of the Order. Always set to \"GUARANTEED_STOP_LOSS\" for Guaranteed Stop Loss Orders.
    """

    price: Annotated[PriceValue, TransportField(...)]
    """
    The price threshold specified for the Guaranteed Stop Loss Order. The
    associated Trade will be closed at this price.
    """

    distance: Annotated[Optional[PriceValue], TransportField(None)]
    """
    Specifies the distance (in price units) from the Account's current price to use as the Stop Loss Order price. If the Trade is short the Instrument's bid price is used, and for long Trades the ask is used.
    """

    time_in_force: Annotated[TimeInForce, TransportField(TimeInForce.GTC, alias="timeInForce")]
    """
    The time-in-force requested for the GuaranteedStopLoss Order. Restricted
    to `GTC`, `GFD` and `GTD` for GuaranteedStopLoss Orders.
    """

__all__ = ("GuaranteedStopLossOrder",)
