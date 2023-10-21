"""ListTrades200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from .trade import Trade

from .response_mixins import LastTransactionResponse
from ..transport.transport_fields import TransportField


class ListTrades200Response(LastTransactionResponse):
    """
    listTrades200Response
    """

    trades: Annotated[Optional[list[Trade]], TransportField(None)]
    """
    The list of Trade detail objects
    """


__all__ = ("ListTrades200Response",)
