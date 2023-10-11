
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Optional


from .position import Position

from ..transport import ApiObject, TransportField
from ..util import exporting


class GetPosition200Response(ApiObject):
    """
    GetPosition200Response
    """
    position: Optional[Position] = TransportField(None)
    """
    The requested Position.
    """
    last_transaction_id: Optional[str] = TransportField(None, alias="lastTransactionID")
    """
    The ID of the most recent Transaction created for the Account
    """


__all__ = exporting(__name__, ...)
