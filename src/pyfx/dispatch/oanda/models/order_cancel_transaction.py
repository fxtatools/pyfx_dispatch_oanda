"""OrderCancelTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal, Optional

from ..transport import TransportField

from .transaction import Transaction
from .transaction_type import TransactionType
from .common_types import OrderId, TradeId, TransactionId
from .order_cancel_reason import OrderCancelReason


class OrderCancelTransaction(Transaction):
    """
    An OrderCancelTransaction represents the cancellation of an Order in the client's Account.

    """

    type: Annotated[Literal[TransactionType.ORDER_CANCEL], TransportField(TransactionType.ORDER_CANCEL)] = TransactionType.ORDER_CANCEL
    """
    The Type of the Transaction. Always set to \"ORDER_CANCEL\" for an OrderCancelTransaction.
    """

    order_id: Annotated[Optional[OrderId], TransportField(None, alias="orderID")]
    """
    The ID of the Order cancelled
    """

    client_order_id: Annotated[Optional[OrderId], TransportField(None, alias="clientOrderID")]
    """
    The client ID of the Order cancelled (only provided if the Order has a client Order ID).
    """

    reason: Annotated[Optional[OrderCancelReason], TransportField(None)]
    """
    The reason that the Order was cancelled.
    """

    replaced_by_order_id: Annotated[Optional[OrderId], TransportField(None, alias="replacedByOrderID")]
    """
    The ID of the Order that replaced this Order (only provided if this Order was cancelled for replacement).
    """

    closed_trade_id: Annotated[Optional[TradeId], TransportField(None, alias="closedTradeID")]
    """
    This field is supplemental to the fxTrade v20 API 3.0.25.
    Value type has been inferred from server response.
    """

    trace_close_transaction_id: Annotated[Optional[TransactionId], TransportField(None, alias="tradeCloseTransactionID")]
    """
    This field is supplemental to the fxTrade v20 API 3.0.25
    Value type has been inferred from server response.
    """

__all__ = ("OrderCancelTransaction",)
