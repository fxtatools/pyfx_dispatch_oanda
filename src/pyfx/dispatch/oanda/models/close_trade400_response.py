"""CloseTrade400Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField

from .response_mixins import ApiErrorResponse
from .market_order_reject_transaction import MarketOrderRejectTransaction


class CloseTrade400Response(ApiErrorResponse):
    """
    CloseTrade400Response
    """

    order_reject_transaction: Annotated[Optional[MarketOrderRejectTransaction], TransportField(None, alias="orderRejectTransaction")]
    """
    The MarketOrderReject Transaction that rejects the creation of the Trade-closing MarketOrder.
    """


__all__ = ("CloseTrade400Response",)
