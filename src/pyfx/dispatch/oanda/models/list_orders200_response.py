"""ListOrders200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.transport_fields import TransportField
from .response_mixins import LastTransactionResponse
from .order import Order


class ListOrders200Response(LastTransactionResponse):
    """
    listOrders200Response
    """

    orders: Annotated[Optional[list[Order]], TransportField(None)]
    """
    The list of Order detail objects
    """


__all__ = ("ListOrders200Response",)
