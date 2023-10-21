"""ListOpenPositions200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.transport_fields import TransportField
from .response_mixins import LastTransactionResponse
from .position import Position


class ListOpenPositions200Response(LastTransactionResponse):
    """
    listOpenPositions200Response
    """

    positions: Annotated[Optional[list[Position]], TransportField(None)]
    """
    The list of open Positions in the Account.
    """


__all__ = ("ListOpenPositions200Response",)
