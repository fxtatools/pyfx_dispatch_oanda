"""GuaranteedStopLossOrderTransaction model definition for OANDA v20 REST API, supplemental to 3.0.25"""

from typing import Annotated, Literal, Optional
from ..transport.transport_fields import TransportField

from .transaction_mixins import OrderStopsTransaction
from .guaranteed_stop_loss_order_reason import GuaranteedStopLossOrderReason
from .transaction_type import TransactionType

from .common_types import PriceValue
from .time_in_force import TimeInForce


class GuaranteedStopLossOrderTransaction(OrderStopsTransaction):
    """A GuaranteedStopLossOrderTransaction represents the creation of a GuaranteedStopLoss Order in the user's Account.

    supplemental to v20 API 3.0.25
    """

    type: Annotated[
        Literal[TransactionType.GUARANTEED_STOP_LOSS_ORDER],
        TransportField(...)
    ] = TransactionType.GUARANTEED_STOP_LOSS_ORDER
    """The Type of the Transaction. Always set to `GUARANTEED_STOP_LOSS_ORDER`
    in a GuaranteedStopLossOrderTransaction.
    """

    time_in_force: Annotated[TimeInForce, TransportField(TimeInForce.GTC, alias="timeInForce")]
    """The time-in-force requested for the GuaranteedStopLoss Order. Restricted
    to `GTC`, `GFD` and `GTD` for GuaranteedStopLoss Orders.
    """

    guaranteedExecutionPremium : Annotated[Optional[PriceValue], TransportField(None)]
    """The fee that will be charged if the Guaranteed Stop Loss Order is filled at the guaranteed price.

    The value is determined at Order creation time. It is in price units and is charged for each unit of the Trade.
    """

    reason : Annotated[GuaranteedStopLossOrderReason, TransportField(...)]
    """The reason that the Guaranteed Stop Loss Order was initiated
    """

__all__ = ("GuaranteedStopLossOrderTransaction",)
