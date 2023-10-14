
"""StopOrderTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal

from ..transport.transport_fields import TransportField

from .transaction_mixins import PriceBoundEntryTransaction
from .transaction_type import TransactionType
from .time_in_force import TimeInForce
from .common_types import PriceValue
from .stop_order_reason import StopOrderReason


class StopOrderTransaction(PriceBoundEntryTransaction):
    """
    A StopOrderTransaction represents the creation of a Stop Order in the user's Account.
    """

    type: Annotated[Literal[TransactionType.STOP_ORDER], TransportField(TransactionType.STOP_ORDER)] = TransactionType.STOP_ORDER
    """
    The Type of the Transaction. Always set to \"STOP_ORDER\" in a StopOrderTransaction.
    """

    price: Annotated[PriceValue, TransportField(...)]
    """
    The price threshold specified for the Stop Order. The Stop Order will only be filled by a market price that is equal to or worse than this price.
    """

    time_in_force: Annotated[TimeInForce, TransportField(TimeInForce.GTC, alias="timeInForce")]
    """
    The time-in-force requested for the Stop Order.
    """

    reason: Annotated[StopOrderReason, TransportField(...)]
    """
    The reason that the Stop Order was initiated
    """


__all__ = ("StopOrderTransaction",)
