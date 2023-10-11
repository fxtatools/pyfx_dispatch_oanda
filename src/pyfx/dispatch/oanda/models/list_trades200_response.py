
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Optional


from .trade import Trade


from ..transport import ApiObject, TransportField
from ..util import exporting


class ListTrades200Response(ApiObject):
    """
    listTrades200Response
    """
    trades: Optional[list[Trade]] = TransportField(None)
    """
    The list of Trade detail objects
    """
    last_transaction_id: Optional[str] = TransportField(None, alias="lastTransactionID")
    """
    The ID of the most recent Transaction created for the Account
    """


__all__ = exporting(__name__, ...)
