
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Annotated, Optional


from .position import Position


from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting


class ListPositions200Response(ApiObject):
    """
    listPositions200Response
    """
    positions: Annotated[Optional[list[Position]], TransportField(None)]
    """
    The list of Account Positions.
    """
    last_transaction_id: Annotated[Optional[str], TransportField(None, alias="lastTransactionID")]
    """
    The ID of the most recent Transaction created for the Account
    """


__all__ = exporting(__name__, ...)
