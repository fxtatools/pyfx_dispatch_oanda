
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Annotated, Optional


from .trade import Trade


from ..transport import ApiObject, TransportField
from ..util import exporting


class ListOpenTrades200Response(ApiObject):
    """
    listOpenTrades200Response
    """
    trades: Annotated[Optional[list[Trade]], TransportField(None)]
    """
    The Account's list of open Trades
    """
    last_transaction_id: Annotated[Optional[str], TransportField(None, alias="lastTransactionID")]
    """
    The ID of the most recent Transaction created for the Account
    """


__all__ = exporting(__name__, ...)
