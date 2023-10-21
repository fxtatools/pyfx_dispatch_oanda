"""SetTradeDependentOrders400Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.transport_fields import TransportField
from .response_mixins import TransactionErrorResponse

from .order_cancel_reject_transaction import OrderCancelRejectTransaction
from .stop_loss_order_reject_transaction import StopLossOrderRejectTransaction
from .take_profit_order_reject_transaction import TakeProfitOrderRejectTransaction
from .trailing_stop_loss_order_reject_transaction import TrailingStopLossOrderRejectTransaction
from .guaranteed_stop_loss_order_reject_transaction import GuaranteedStopLossOrderRejectTransaction


class SetTradeDependentOrders400Response(TransactionErrorResponse):
    """
    SetTradeDependentOrders400Response
    """

    take_profit_order_cancel_reject_transaction: Annotated[Optional[OrderCancelRejectTransaction], TransportField(None, alias="takeProfitOrderCancelRejectTransaction")]
    """An OrderCancelRejectTransaction represents the rejection of the cancellation of an
    Order in the client's Account.
    """

    take_profit_order_reject_transaction: Annotated[Optional[TakeProfitOrderRejectTransaction], TransportField(None, alias="takeProfitOrderRejectTransaction")]
    """ A TakeProfitOrderRejectTransaction represents the rejection of the creation of a
    TakeProfit Order.
    """

    stop_loss_order_cancel_reject_transaction: Annotated[Optional[OrderCancelRejectTransaction], TransportField(None, alias="stopLossOrderCancelRejectTransaction")]
    """An OrderCancelRejectTransaction represents the rejection of the cancellation of an
    Order in the client's Account.
    """

    stop_loss_order_reject_transaction: Annotated[Optional[StopLossOrderRejectTransaction], TransportField(None, alias="stopLossOrderRejectTransaction")]
    """A StopLossOrderRejectTransaction represents the rejection of the creation of a
    StopLoss Order.
    """

    trailing_stop_loss_order_cancel_reject_transaction: Annotated[Optional[OrderCancelRejectTransaction], TransportField(None, alias="trailingStopLossOrderCancelRejectTransaction")]
    """An OrderCancelRejectTransaction represents the rejection of the cancellation of
    an Order in the client's Account.
    """

    trailing_stop_loss_order_reject_transaction: Annotated[Optional[TrailingStopLossOrderRejectTransaction], TransportField(None, alias="trailingStopLossOrderRejectTransaction")]
    """A TrailingStopLossOrderRejectTransaction represents the rejection of the creation of
    a TrailingStopLoss Order.
    """

    guaranteed_stop_loss_order_cancel_reject_transaction: Annotated[Optional[OrderCancelRejectTransaction], TransportField(None, alias="guaranteedStopLossOrderCancelRejectTransaction")]
    """An OrderCancelRejectTransaction represents the rejection of the cancellation of an
    Order in the client's Account.

    supplemental to the fxTrade v20 API 3.0.25
    """

    guaranteed_stop_loss_order_reject_transaction: Annotated[Optional[GuaranteedStopLossOrderRejectTransaction], TransportField(None, alias="guaranteedStopLossOrderRejectTransaction")]
    """
    A GuaranteedStopLossOrderRejectTransaction represents the rejection of the creation of
    a GuaranteedStopLoss Order.

    supplemental to the fxTrade v20 API 3.0.25
    """


__all__ = ("SetTradeDependentOrders400Response",)
