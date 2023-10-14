
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Annotated, Optional


from .order import Order


from ..transport import ApiObject, TransportField
from ..util import exporting


class ListOrders200Response(ApiObject):
    """
    listOrders200Response
    """
    orders: Annotated[Optional[list[Order]], TransportField(None)]
    """
    The list of Order detail objects
    """
    last_transaction_id: Annotated[Optional[str], TransportField(None, alias="lastTransactionID")]
    """
    The ID of the most recent Transaction created for the Account
    """


__all__ = exporting(__name__, ...)
