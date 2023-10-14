
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Annotated, Optional


from .transaction import Transaction


from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting


class GetTransactionRange200Response(ApiObject):
    """
    GetTransactionRange200Response
    """
    transactions: Annotated[Optional[list[Transaction]], TransportField(None)]
    """
    The list of Transactions that satisfy the request.
    """
    last_transaction_id: Annotated[Optional[str], TransportField(None, alias="lastTransactionID")]
    """
    The ID of the most recent Transaction created for the Account
    """


__all__ = exporting(__name__, ...)
