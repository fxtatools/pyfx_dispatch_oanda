"""CancelOrder200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Optional

from ..transport import TransportField

from .response_mixins import TransactionResponse
from .order_cancel_transaction import OrderCancelTransaction


class CancelOrder200Response(TransactionResponse):
    """
    CancelOrder200Response: The Order was cancelled as specified
    """

    order_cancel_transaction: Optional[OrderCancelTransaction] = TransportField(
        None, alias="orderCancelTransaction")
    """
    The Transaction that cancelled the Order
    """


__all__ = ("CancelOrder200Response",)
