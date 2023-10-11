"""CancelOrder404Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Optional

from ..transport import TransportField

from .order_cancel_reject_transaction import OrderCancelRejectTransaction
from .response_mixins import TransactionErrorResponse


class CancelOrder404Response(TransactionErrorResponse):
    """
    CancelOrder404Response: The Account or Order specified does not exist. 
    """

    order_cancel_reject_transaction: Optional[OrderCancelRejectTransaction] = TransportField(
        None, alias="orderCancelRejectTransaction")
    """The Transaction that rejected the cancellation of the Order. Only present if the Account exists.
    """


__all__ = ("CancelOrder404Response",)
