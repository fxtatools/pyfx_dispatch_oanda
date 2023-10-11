"""CloseTrade400Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Optional

from ..transport import ApiObject, TransportField

from .response_mixins import ErrorResponse
from .market_order_reject_transaction import MarketOrderRejectTransaction


class CloseTrade400Response(ErrorResponse):
    """
    CloseTrade400Response
    """

    order_reject_transaction: Optional[MarketOrderRejectTransaction] = TransportField(None, alias="orderRejectTransaction")
    """
    The MarketOrderReject Transaction that rejects the creation of the Trade-closing MarketOrder.
    """


__all__ = ("CloseTrade400Response",)
