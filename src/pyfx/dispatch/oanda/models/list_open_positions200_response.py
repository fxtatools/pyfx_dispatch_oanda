
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Annotated, Optional


from .position import Position


from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting


class ListOpenPositions200Response(ApiObject):
    """
    listOpenPositions200Response
    """
    positions: Annotated[Optional[list[Position]], TransportField(None)]
    """
    The list of open Positions in the Account.
    """
    last_transaction_id: Annotated[Optional[str], TransportField(None, alias="lastTransactionID")]
    """
    The ID of the most recent Transaction created for the Account
    """


__all__ = exporting(__name__, ...)
