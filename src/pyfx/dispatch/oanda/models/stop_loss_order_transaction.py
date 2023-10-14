"""StopLossOrderTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal, Optional


from ..transport.transport_fields import TransportField

from .transaction_mixins import OrderDistanceStopsTransaction

from .transaction_type import TransactionType
from .time_in_force import TimeInForce
from .stop_loss_order_reason import StopLossOrderReason

from .common_types import PriceValue, FloatValue


class StopLossOrderTransaction(OrderDistanceStopsTransaction):
    """
    A StopLossOrderTransaction represents the creation of a StopLoss Order in the user's Account.

    """

    type: Annotated[Literal[TransactionType.STOP_LOSS_ORDER], TransportField(TransactionType.STOP_LOSS_ORDER)] = TransactionType.STOP_LOSS_ORDER
    """
    The Type of the Transaction. Always set to \"STOP_LOSS_ORDER\" in a StopLossOrderTransaction.
    """

    price: Annotated[PriceValue, TransportField(...)]
    """
    The price threshold specified for the Stop Loss Order. The associated Trade will be closed by a market price that is equal to or worse than this threshold.
    """

    time_in_force: Annotated[TimeInForce, TransportField(TimeInForce.GTC, alias="timeInForce")]
    """
    The time-in-force requested for the StopLoss Order. Restricted to \"GTC\", \"GFD\" and \"GTD\" for StopLoss Orders.
    """

    reason: Annotated[StopLossOrderReason, TransportField(...)]
    """
    The reason that the Stop Loss Order was initiated
    """

    guaranteed: Annotated[Optional[bool], TransportField(None)]
    """
    Flag indicating that the Stop Loss Order is guaranteed. The default value depends on the GuaranteedStopLossOrderMode of the account, if it is REQUIRED, the default will be true, for DISABLED or ENABLED the default is false.
    """

    guaranteed_execution_premium: Annotated[Optional[FloatValue], TransportField(None, alias="guaranteedExecutionPremium", deprecated=True)]
    """
    The fee that will be charged if the Stop Loss Order is guaranteed and the Order is filled at the guaranteed price. The value is determined at Order creation time. It is in price units and is charged for each unit of the Trade.
    """

    trigger_mode: Annotated[Optional[str], TransportField(None, alias="triggerMode")]
    """
    This field is supplemental to the fxTrade v20 API 3.0.25.
    Value type has been inferred from server response.
    
    Known values: `"TOP_OF_BOOK"`
    """


__all__ = ("StopLossOrderTransaction",)
