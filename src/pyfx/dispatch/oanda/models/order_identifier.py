
"""OrderIdentifier model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport import ApiObject, TransportField

from .common_types import OrderId, ClientId


class OrderIdentifier(ApiObject):
    """
    An OrderIdentifier is used to refer to an Order, and contains both the OrderID and the ClientOrderID.
    """

    order_id: Annotated[OrderId, TransportField(...,  alias="orderID")]
    """
    The OANDA-assigned Order ID
    """

    client_order_id: Annotated[Optional[ClientId], TransportField(None, alias="clientOrderID")]
    """
    The client-provided client Order ID
    """

__all__ = ("OrderIdentifier",)
