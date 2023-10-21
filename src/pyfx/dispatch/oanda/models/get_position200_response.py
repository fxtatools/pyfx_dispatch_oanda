"""GetPosition200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated

from ..transport.transport_fields import TransportField
from .response_mixins import LastTransactionResponse
from .position import Position


class GetPosition200Response(LastTransactionResponse):
    """
    GetPosition200Response
    """

    position: Annotated[Position, TransportField(...)]
    """
    The requested Position.
    """


__all__ = ("GetPosition200Response",)
