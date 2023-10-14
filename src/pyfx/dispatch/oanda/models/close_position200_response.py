"""ClosePosition200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport import TransportField

from .market_order_transaction import MarketOrderTransaction
from .order_cancel_transaction import OrderCancelTransaction
from .order_fill_transaction import OrderFillTransaction

from .response_mixins import TransactionResponse


class ClosePosition200Response(TransactionResponse):
    """
    ClosePosition200Response: The Position closeout request has been successfully processed.
    """

    long_order_create_transaction: Annotated[Optional[MarketOrderTransaction], TransportField(None, alias="longOrderCreateTransaction")]
    """
    The MarketOrderTransaction created to close the long Position.
    """

    long_order_fill_transaction: Annotated[Optional[OrderFillTransaction], TransportField(None, alias="longOrderFillTransaction")]
    """
    OrderFill Transaction that closes the long Position
    """

    long_order_cancel_transaction: Annotated[Optional[OrderCancelTransaction], TransportField(None, alias="longOrderCancelTransaction")]
    """
    OrderCancel Transaction that cancels the MarketOrder created to close the long Position
    """

    short_order_create_transaction: Annotated[Optional[MarketOrderTransaction], TransportField(None, alias="shortOrderCreateTransaction")]
    """
    The MarketOrderTransaction created to close the short Position.
    """

    short_order_fill_transaction: Annotated[Optional[OrderFillTransaction], TransportField(None, alias="shortOrderFillTransaction")]
    """
    OrderFill Transaction that closes the short Position
    """

    short_order_cancel_transaction: Annotated[Optional[OrderCancelTransaction], TransportField(None, alias="shortOrderCancelTransaction")]
    """
    OrderCancel Transaction that cancels the MarketOrder created to close the short Position
    """


__all__ = ("ClosePosition200Response",)
