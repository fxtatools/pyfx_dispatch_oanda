
"""Order model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.data import AbstractApiObject
from ..transport.transport_fields import TransportField

from .common_types import OrderId, Time
from .client_extensions import ClientExtensions

from .order_state import OrderState
from .order_type import OrderType


class Order(AbstractApiObject, # type: ignore
            designator_key="type",
            designator_type=OrderType):
    """
    The base Order definition specifies the properties that are common to all Orders.
    """

    id: Annotated[OrderId, TransportField(...)]
    """
    The Order's identifier, unique within the Order's Account.
    """

    create_time: Annotated[Time, TransportField(..., alias="createTime")]
    """
    The time when the Order was created.
    """

    state: Annotated[OrderState, TransportField(...)]
    """
    The current state of the Order.
    """

    client_extensions: Annotated[Optional[ClientExtensions], TransportField(None, alias="clientExtensions")]
    """
    The client extensions of the Order. Do not set, modify, or delete
    clientExtensions if your account is associated with MT4.
    """

__all__ = ("Order",)
