"""CreateOrderRequest model definition for OANDA v20 REST API (3.0.25)"""

from ..transport.data import AbstractApiObject

from .order_type import OrderType


class CreateOrderRequest(AbstractApiObject, 
                         designator_key="type",
                         designator_type=OrderType):
    """
    CreateOrderRequest (abstract REST API class, fxTrade v20)
    
    Similar Classes:
    - MarketOrderRequest
    - LimitOrderRequest
    - StopOrderRequest
    - MarketIfTouchedOrderRequest
    - TakeProfitOrderRequest
    - StopLossOrderRequest
    - GuaranteedStopLossOrderRequest
    - TrailingStopLossOrderRequest
    """

    # order: Optional[dict[str, Any]] = TransportField(None)
    # """
    # The base Order specification used when requesting that an Order be created. Each specific Order-type extends this definition.
    # """


__all__ = ("CreateOrderRequest",)
