
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Optional


from .order import Order

from ..transport import ApiObject, TransportField
from ..util import exporting


class GetOrder200Response(ApiObject):
    """
    GetOrder200Response
    """
    order: Optional[Order] = TransportField(None)
    """
    The details of the Order requested
    """
    last_transaction_id: Optional[str] = TransportField(None, alias="lastTransactionID")
    """
    The ID of the most recent Transaction created for the Account
    """


__all__ = exporting(__name__, ...)
