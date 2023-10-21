"""GetTransactionRange200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from .response_mixins import LastTransactionResponse
from .transaction import Transaction
from ..transport.transport_fields import TransportField


class GetTransactionRange200Response(LastTransactionResponse):
    """
    GetTransactionRange200Response
    """

    transactions: Annotated[Optional[list[Transaction]], TransportField(None)]
    """
    The list of Transactions that satisfy the request.
    """


__all__ = ("GetTransactionRange200Response",)
