"""ListOpenTrades200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.transport_fields import TransportField
from .response_mixins import LastTransactionResponse
from .trade import Trade


class ListOpenTrades200Response(LastTransactionResponse):
    """
    listOpenTrades200Response
    """

    trades: Annotated[Optional[list[Trade]], TransportField(None)]
    """
    The Account's list of open Trades
    """


__all__ = ("ListOpenTrades200Response",)
