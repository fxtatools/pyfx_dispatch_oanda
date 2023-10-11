
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Optional


from .transaction import Transaction


from ..transport import ApiObject, TransportField
from ..util import exporting


class GetTransactionRange200Response(ApiObject):
    """
    GetTransactionRange200Response
    """
    transactions: Optional[list[Transaction]] = TransportField(None)
    """
    The list of Transactions that satisfy the request.
    """
    last_transaction_id: Optional[str] = TransportField(None, alias="lastTransactionID")
    """
    The ID of the most recent Transaction created for the Account
    """


__all__ = exporting(__name__, ...)
