"""ReplaceOrder400Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.transport_fields import TransportField
from .response_mixins import TransactionErrorResponse
from .transaction import Transaction


class ReplaceOrder400Response(TransactionErrorResponse):
    """
    ReplaceOrder400Response
    """

    order_reject_transaction: Annotated[Optional[Transaction], TransportField(None, alias="orderRejectTransaction")]
    """The Transaction that rejected the creation of the replacing Orde
    """

__all__ = ("ReplaceOrder400Response",)
