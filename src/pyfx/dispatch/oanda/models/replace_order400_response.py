
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Annotated, Optional


from .transaction import Transaction


from ..transport import ApiObject, TransportField
from ..util import exporting


class ReplaceOrder400Response(ApiObject):
    """
    ReplaceOrder400Response
    """
    order_reject_transaction: Annotated[Optional[Transaction], TransportField(None, alias="orderRejectTransaction")]
    related_transaction_ids: Annotated[Optional[list[str]], TransportField(None, alias="relatedTransactionIDs")]
    """
    The IDs of all Transactions that were created while satisfying the request.
    """
    last_transaction_id: Annotated[Optional[str], TransportField(None, alias="lastTransactionID")]
    """
    The ID of the most recent Transaction created for the Account.
    """
    error_code: Annotated[Optional[str], TransportField(None, alias="errorCode")]
    """
    The code of the error that has occurred. This field may not be returned for some errors.
    """
    error_message: Annotated[Optional[str], TransportField(None, alias="errorMessage")]
    """
    The human-readable description of the error that has occurred.
    """


__all__ = exporting(__name__, ...)
