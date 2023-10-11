
"""model definition for OANDA v20 REST API (3.0.25)"""




from typing import Optional


from .account import Account

from ..transport import ApiObject, TransportField
from ..util import exporting



class GetAccount200Response(ApiObject):
    """
    GetAccount200Response
    """
    account: Optional[Account] = TransportField(None)
    """The full details of the requested Account.
    """
    last_transaction_id: Optional[str] = TransportField(None, alias="lastTransactionID")
    """The ID of the most recent Transaction created for the Account.
    """


__all__ = exporting(__name__, ...)

