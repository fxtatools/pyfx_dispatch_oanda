
"""LimitOrderTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal

from ..transport.transport_fields import TransportField

from .transaction_mixins import PriceEntryTransaction, ReplacementTxn

from .transaction_type import TransactionType
from .common_types import PriceValue
from .time_in_force import TimeInForce
from .limit_order_reason import LimitOrderReason


class LimitOrderTransaction(PriceEntryTransaction, ReplacementTxn):
    """
    A LimitOrderTransaction represents the creation of a Limit Order in the user's Account.
    """

    type: Annotated[Literal[TransactionType.LIMIT_ORDER], TransportField(TransactionType.LIMIT_ORDER)] = TransactionType.LIMIT_ORDER
    """
    The Type of the Transaction. Always set to \"LIMIT_ORDER\" in a LimitOrderTransaction.
    """

    price: Annotated[PriceValue, TransportField(...)]
    """
    The price threshold specified for the Limit Order. The Limit Order will only be filled by a market price that is equal to or better than this price.
    """

    time_in_force: Annotated[TimeInForce, TransportField(TimeInForce.GTC, alias="timeInForce")]
    """
    The time-in-force requested for the Limit Order.
    """

    reason: Annotated[LimitOrderReason, TransportField(...)]
    """
    The reason that the Limit Order was initiated
    """

__all__ = ("LimitOrderTransaction",)
