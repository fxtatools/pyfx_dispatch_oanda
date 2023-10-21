"""ReplaceOrder404Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.transport_fields import TransportField
from .response_mixins import TransactionErrorResponse
from .transaction import Transaction


class ReplaceOrder404Response(TransactionErrorResponse):
    """
    ReplaceOrder404Response
    """

    order_cancel_reject_transaction: Annotated[Optional[Transaction], TransportField(None, alias="orderCancelRejectTransaction")]
    """The Transaction that rejected the cancellation of the Order to be replaced.

    Only present if the Account exists.
    """


__all__ = ("ReplaceOrder404Response",)
