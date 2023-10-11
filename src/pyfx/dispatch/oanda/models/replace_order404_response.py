
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Optional


from .transaction import Transaction


from ..transport import ApiObject, TransportField
from ..util import exporting


class ReplaceOrder404Response(ApiObject):
    """
    ReplaceOrder404Response
    """
    order_cancel_reject_transaction: Optional[Transaction] = TransportField(None, alias="orderCancelRejectTransaction")
    related_transaction_ids: Optional[list[str]] = TransportField(None, alias="relatedTransactionIDs")
    """
    The IDs of all Transactions that were created while satisfying the request. Only present if the Account exists.
    """
    last_transaction_id: Optional[str] = TransportField(None, alias="lastTransactionID")
    """
    The ID of the most recent Transaction created for the Account. Only present if the Account exists.
    """
    error_code: Optional[str] = TransportField(None, alias="errorCode")
    """
    The code of the error that has occurred. This field may not be returned for some errors.
    """
    error_message: Optional[str] = TransportField(None, alias="errorMessage")
    """
    The human-readable description of the error that has occurred.
    """


__all__ = exporting(__name__, ...)
