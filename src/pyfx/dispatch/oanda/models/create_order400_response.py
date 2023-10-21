
"""model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.transport_fields import TransportField

from .transaction import Transaction
from .response_mixins import TransactionErrorResponse


class CreateOrder400Response(TransactionErrorResponse):
    """
    CreateOrder400Response
    """

    order_reject_transaction: Annotated[Optional[Transaction], TransportField(None, alias="orderRejectTransaction")]
    """The Transaction that rejected the creation of the Order as requested"""


__all__ = ("CreateOrder400Response",)
