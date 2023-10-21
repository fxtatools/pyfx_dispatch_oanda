"""GetTrade200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated

from .trade import Trade

from ..transport.transport_fields import TransportField
from .response_mixins import LastTransactionResponse


class GetTrade200Response(LastTransactionResponse):
    """
    GetTrade200Response
    """

    trade: Annotated[Trade, TransportField(...)]
    """
    The details of the requested trade
    """


__all__ = ("GetTrade200Response",)
