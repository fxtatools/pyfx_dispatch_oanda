
"""CancelOrder200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Optional

from .response_mixins import TransactionResponse

from ..transport import TransportField

from .order_cancel_transaction import OrderCancelTransaction
from .response_mixins import TransactionResponse


class CancelOrder200Response(TransactionResponse):
    """
    CancelOrder200Response: The Order was cancelled as specified
    """

    order_cancel_transaction: Optional[OrderCancelTransaction] = TransportField(
        None, alias="orderCancelTransaction")
    """The Transaction that cancelled the Order
    """


__all__ = ("CancelOrder200Response",)
