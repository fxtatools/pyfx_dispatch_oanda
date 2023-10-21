"""GetTransaction200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated

from ..transport.transport_fields import TransportField
from .response_mixins import LastTransactionResponse
from .transaction import Transaction


class GetTransaction200Response(LastTransactionResponse):
    """
    GetTransaction200Response
    """

    transaction: Annotated[Transaction, TransportField(...)]
    """
    The details of the Transaction requested
    """


__all__ = ("GetTransaction200Response",)
