
"""model definition for OANDA v20 REST API (3.0.25)"""

from typing import Any, Optional

from ..transport import ApiObject, TransportField
from ..util import exporting


class CreateOrderRequest(ApiObject):
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
    ## dict is a diffiult type here
    # order: Optional[dict[str, Any]] = TransportField(None)
    # """
    # The base Order specification used when requesting that an Order be created. Each specific Order-type extends this definition.
    # """


__all__ = exporting(__name__, ...)
