"""CloseTrade200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Optional

from ..transport import TransportField

from .response_mixins import TransactionResponse
from .market_order_transaction import MarketOrderTransaction
from .order_cancel_transaction import OrderCancelTransaction
from .order_fill_transaction import OrderFillTransaction


class CloseTrade200Response(TransactionResponse):
    """
    CloseTrade200Response: The Trade has been closed as requested
    """

    order_create_transaction: Optional[MarketOrderTransaction] = TransportField(None, alias="orderCreateTransaction")
    """
    The MarketOrder Transaction created to close the Trade.
    """

    order_fill_transaction: Optional[OrderFillTransaction] = TransportField(None, alias="orderFillTransaction")
    """
    The OrderFill Transaction that fills the Trade-closing MarketOrder and closes the Trade.
    """

    order_cancel_transaction: Optional[OrderCancelTransaction] = TransportField(None, alias="orderCancelTransaction")
    """
    The OrderCancel Transaction that immediately cancelled the Trade-closing MarketOrder.
    """


__all__ = ("CloseTrade200Response",)
