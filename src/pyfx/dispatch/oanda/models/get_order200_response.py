"""model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated

from ..transport.transport_fields import TransportField

from .order import Order
from .response_mixins import LastTransactionResponse


class GetOrder200Response(LastTransactionResponse):
    """
    GetOrder200Response
    """

    order: Annotated[Order, TransportField(...)]
    """
    The details of the Order requested
    """


__all__ = ("GetOrder200Response",)
