
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Optional


from .transaction import Transaction

from ..transport import ApiObject, TransportField
from ..util import exporting


class GetTransaction200Response(ApiObject):
    """
    GetTransaction200Response
    """
    transaction: Optional[Transaction] = TransportField(None)
    """
    The details of the Transaction requested
    """
    last_transaction_id: Optional[str] = TransportField(None, alias="lastTransactionID")
    """
    The ID of the most recent Transaction created for the Account
    """


__all__ = exporting(__name__, ...)
