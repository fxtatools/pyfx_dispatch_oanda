"""GetAccount200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional
from ..transport.transport_fields import TransportField

from .response_mixins import LastTransactionResponse
from .account import Account


class GetAccount200Response(LastTransactionResponse):
    """
    GetAccount200Response
    """

    account: Annotated[Optional[Account], TransportField(None)]
    """The full details of the requested Account."""


__all__ = ("GetAccount200Response",)
