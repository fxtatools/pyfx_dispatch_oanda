
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Optional


from .position import Position


from ..transport import ApiObject, TransportField
from ..util import exporting


class ListOpenPositions200Response(ApiObject):
    """
    listOpenPositions200Response
    """
    positions: Optional[list[Position]] = TransportField(None)
    """
    The list of open Positions in the Account.
    """
    last_transaction_id: Optional[str] = TransportField(None, alias="lastTransactionID")
    """
    The ID of the most recent Transaction created for the Account
    """


__all__ = exporting(__name__, ...)
