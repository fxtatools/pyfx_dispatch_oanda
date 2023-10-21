"""ListPendingOrders200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from .order import Order

from .response_mixins import LastTransactionResponse
from ..transport.transport_fields import TransportField


class ListPendingOrders200Response(LastTransactionResponse):
    """
    listPendingOrders200Response
    """

    orders: Annotated[Optional[list[Order]], TransportField(None)]
    """
    The list of pending Order details
    """


__all__ = ("ListPendingOrders200Response",)
