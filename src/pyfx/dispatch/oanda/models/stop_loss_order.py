
"""StopLossOrder model definition for OANDA v20 REST API (3.0.25)"""


from typing import Annotated, Literal, Optional

from ..transport.transport_fields import TransportField

from .common_types import PriceValue
from .order_mixins import LimitOrderMixin
from .trade_id_mixin import TradeIdMixin
from .order_mixins import ReplacesOrderMixin
from .order_type import OrderType
from .time_in_force import TimeInForce


class StopLossOrder(LimitOrderMixin, TradeIdMixin, ReplacesOrderMixin):
    """
    A StopLossOrder is an order that is linked to an open Trade and created with a price threshold. The Order will be filled (closing the Trade) by the first price that is equal to or worse than the threshold. A StopLossOrder cannot be used to open a new Position.
    """

    type: Annotated[Literal[OrderType.STOP_LOSS], TransportField(OrderType.STOP_LOSS)] = OrderType.STOP_LOSS
    """
    The type of the Order. Always set to \"STOP_LOSS\" for Stop Loss Orders.
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

    guaranteed_execution_premium: Annotated[Optional[PriceValue], TransportField(None, deprecated=True, alias="guaranteedExecutionPremium")]
    """
    The premium that will be charged if the Stop Loss Order is guaranteed and the Order is filled at the guaranteed price. It is in price units and is charged for each unit of the Trade.
    """

__all__ = ("StopLossOrder",)
