
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Annotated, Optional


from .order_client_extensions_modify_reject_transaction import OrderClientExtensionsModifyRejectTransaction


from ..transport import ApiObject, TransportField
from ..util import exporting


class SetOrderClientExtensions400Response(ApiObject):
    """
    SetOrderClientExtensions400Response
    """
    order_client_extensions_modify_reject_transaction: Annotated[Optional[OrderClientExtensionsModifyRejectTransaction], TransportField(None, alias="orderClientExtensionsModifyRejectTransaction")]
    last_transaction_id: Annotated[Optional[str], TransportField(None, alias="lastTransactionID")]
    """
    The ID of the most recent Transaction created for the Account
    """
    related_transaction_ids: Annotated[Optional[list[str]], TransportField(None, alias="relatedTransactionIDs")]
    """
    The IDs of all Transactions that were created while satisfying the request.
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
