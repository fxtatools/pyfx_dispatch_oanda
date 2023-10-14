
"""StopLossOrderRequest model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal, Optional

from ..transport.transport_fields import TransportField

from .request_mixins import StopsRequestBase
from .common_types import PriceValue
from .order_type import OrderType
from .time_in_force import TimeInForce


class StopLossOrderRequest(StopsRequestBase):
    """
    A StopLossOrderRequest specifies the parameters that may be set when creating a Stop Loss Order. Only one of the price and distance fields may be specified.
    """

    type: Annotated[Literal[OrderType.STOP_LOSS], TransportField(OrderType.STOP_LOSS)] = OrderType.STOP_LOSS
    """
    The type of the Order to Create. Must be set to \"STOP_LOSS\" when creating a Stop Loss Order.
    """

    price: Annotated[PriceValue, TransportField(...)]
    """
    The price threshold specified for the Stop Loss Order. If the guaranteed flag is false, the associated Trade will be closed by a market price that is equal to or worse than this threshold. If the flag is true the associated Trade will be closed at this price.
    """

    distance: Annotated[Optional[PriceValue], TransportField(None)]
    """
    Specifies the distance (in price units) from the Account's current price to use as the Stop Loss Order price. If the Trade is short the Instrument's bid price is used, and for long Trades the ask is used.
    """

    time_in_force: Annotated[TimeInForce, TransportField(TimeInForce.GTC, alias="timeInForce")]
    """
    The time-in-force requested for the StopLoss Order. Restricted to \"GTC\", \"GFD\" and \"GTD\" for StopLoss Orders.
    """

    guaranteed: Annotated[Optional[bool], TransportField(None, deprecated=True)]
    """
    Flag indicating that the Stop Loss Order is guaranteed. The default value depends on the GuaranteedStopLossOrderMode of the account, if it is REQUIRED, the default will be true, for DISABLED or ENABLED the default is false.
    """


__all__ = ("StopLossOrderRequest",)
