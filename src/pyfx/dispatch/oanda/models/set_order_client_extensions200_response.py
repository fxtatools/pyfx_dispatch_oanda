
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Optional


from .order_client_extensions_modify_transaction import OrderClientExtensionsModifyTransaction


from ..transport import ApiObject, TransportField
from ..util import exporting


class SetOrderClientExtensions200Response(ApiObject):
    """
    SetOrderClientExtensions200Response
    """
    order_client_extensions_modify_transaction: Optional[OrderClientExtensionsModifyTransaction] = TransportField(None, alias="orderClientExtensionsModifyTransaction")
    last_transaction_id: Optional[str] = TransportField(None, alias="lastTransactionID")
    """
    The ID of the most recent Transaction created for the Account
    """
    related_transaction_ids: Optional[list[str]] = TransportField(None, alias="relatedTransactionIDs")
    """
    The IDs of all Transactions that were created while satisfying the request.
    """


__all__ = exporting(__name__, ...)
