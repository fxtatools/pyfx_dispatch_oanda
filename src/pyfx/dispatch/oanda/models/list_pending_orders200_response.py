
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Optional


from .order import Order


from ..transport import ApiObject, TransportField
from ..util import exporting


class ListPendingOrders200Response(ApiObject):
    """
    listPendingOrders200Response
    """
    orders: Optional[list[Order]] = TransportField(None)
    """
    The list of pending Order details
    """
    last_transaction_id: Optional[str] = TransportField(None, alias="lastTransactionID")
    """
    The ID of the most recent Transaction created for the Account
    """


__all__ = exporting(__name__, ...)
