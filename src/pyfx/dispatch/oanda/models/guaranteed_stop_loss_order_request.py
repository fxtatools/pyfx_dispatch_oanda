"""GuaranteedStopLossOrderRequest model definition, supplemental to v20 API 3.0.25"""

from typing import Literal, Optional

from ..transport import TransportField

from .request_mixins import StopsRequestBase

from .common_types import PriceValue
from .order_type import OrderType
from .time_in_force import TimeInForce


class GuaranteedStopLossOrderRequest(StopsRequestBase):

    type: Literal[OrderType.GUARANTEED_STOP_LOSS] = TransportField(OrderType.GUARANTEED_STOP_LOSS)
    """
    The type of the Order to Create. Must be set to “GUARANTEED_STOP_LOSS”
    when creating a Guaranteed Stop Loss Order.
    """

    price: PriceValue = TransportField(...)
    """
    The price threshold specified for the Guaranteed Stop Loss Order. The
    associated Trade will be closed at this price.
    """

    distance: Optional[PriceValue] = TransportField(None)
    """
    Specifies the distance (in price units) from the Account’s current price
    to use as the Guaranteed Stop Loss Order price. If the Trade is short the
    Instrument’s bid price is used, and for long Trades the ask is used.
    """

    time_in_force: TimeInForce = TransportField(TimeInForce.GTC, alias="timeInForce")
    """
    The time-in-force requested for the GuaranteedStopLoss Order. Restricted
    to “GTC”, “GFD” and “GTD” for GuaranteedStopLoss Orders.
    """


__all__ = ("GuaranteedStopLossOrderRequest",)
