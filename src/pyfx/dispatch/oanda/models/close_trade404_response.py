
"""CloseTrade404Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport import TransportField

from .response_mixins import TransactionErrorResponse
from .market_order_reject_transaction import MarketOrderRejectTransaction


class CloseTrade404Response(TransactionErrorResponse):
    """
    CloseTrade404Response
    """

    order_reject_transaction: Annotated[Optional[MarketOrderRejectTransaction], TransportField(None, alias="orderRejectTransaction")]
    " The MarketOrderReject Transaction that rejects the creation of the Trade-closing MarketOrder. Only present if the Account exists."


__all__ = ("CloseTrade404Response",)
