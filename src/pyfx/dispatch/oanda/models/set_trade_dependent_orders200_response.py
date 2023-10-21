"""SetTradeDependentOrders200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.transport_fields import TransportField
from .response_mixins import TransactionResponse
from .order_cancel_transaction import OrderCancelTransaction
from .order_fill_transaction import OrderFillTransaction
from .stop_loss_order_transaction import StopLossOrderTransaction
from .take_profit_order_transaction import TakeProfitOrderTransaction
from .trailing_stop_loss_order_transaction import TrailingStopLossOrderTransaction
from .guaranteed_stop_loss_order_transaction import GuaranteedStopLossOrderTransaction


class SetTradeDependentOrders200Response(TransactionResponse):
    """
    SetTradeDependentOrders200Response
    """

    take_profit_order_cancel_transaction: Annotated[
        Optional[OrderCancelTransaction],
        TransportField(None, alias="takeProfitOrderCancelTransaction")
    ]
    """The Transaction created that cancels the Trade's existing Take Profit Order.
    """

    take_profit_order_transaction: Annotated[
        Optional[TakeProfitOrderTransaction],
        TransportField(None, alias="takeProfitOrderTransaction")
    ]
    """The Transaction created that creates a new Take Profit Order for the Trade.
    """

    take_profit_order_fill_transaction: Annotated[
        Optional[OrderFillTransaction],
        TransportField(None, alias="takeProfitOrderFillTransaction")
    ]
    """The Transaction created that immediately fills the Trade's new Take Profit Order.

    Only provided if the new Take Profit Order was immediately filled.
    """

    take_profit_order_created_cancel_transaction: Annotated[
        Optional[OrderCancelTransaction],
        TransportField(None, alias="takeProfitOrderCreatedCancelTransaction")
    ]
    """The Transaction created that immediately cancels the Trade's new Take Profit Order.

    Only provided if the new Take Profit Order was immediately cancelled.
    """

    stop_loss_order_cancel_transaction: Annotated[
        Optional[OrderCancelTransaction],
        TransportField(None, alias="stopLossOrderCancelTransaction")
    ]
    """ The Transaction created that cancels the Trade's existing Stop Loss Order.
    """

    stop_loss_order_transaction: Annotated[
        Optional[StopLossOrderTransaction],
        TransportField(None, alias="stopLossOrderTransaction")
    ]
    """The Transaction created that creates a new Stop Loss Order for the Trade.
    """

    stop_loss_order_fill_transaction: Annotated[
        Optional[OrderFillTransaction],
        TransportField(None, alias="stopLossOrderFillTransaction")
    ]
    """The Transaction created that immediately fills the Trade's new Stop Order.

    Only provided if the new Stop Loss Order was immediately filled.
    """

    stop_loss_order_created_cancel_transaction: Annotated[
        Optional[OrderCancelTransaction],
        TransportField(None, alias="stopLossOrderCreatedCancelTransaction")
    ]
    """The Transaction created that immediately cancels the Trade's new Stop Loss Order.

    Only provided if the new Stop Loss Order was immediately cancelled.
    """

    trailing_stop_loss_order_cancel_transaction: Annotated[
        Optional[OrderCancelTransaction],
        TransportField(None, alias="trailingStopLossOrderCancelTransaction")
    ]
    """The Transaction created that cancels the Trade's existing Trailing Stop Loss Order.
    """

    trailing_stop_loss_order_transaction: Annotated[
        Optional[TrailingStopLossOrderTransaction],
        TransportField(None, alias="trailingStopLossOrderTransaction")
    ]
    """The Transaction created that creates a new Trailing Stop Loss Order for the Trade.
    """

    guaranteed_stop_loss_order_cancel_transaction: Annotated[
        Optional[OrderCancelTransaction],
        TransportField(None, alias="guaranteedStopLossOrderCancelTransaction")
    ]
    """The Transaction created that cancels the Trade's existing Guaranteed Stop Loss Order.

    supplemental to v20 API 3.0.25
    """

    guaranteed_stop_loss_order_transaction: Annotated[
        Optional[GuaranteedStopLossOrderTransaction],
        TransportField(None, alias="guaranteedStopLossOrderTransaction")
    ]
    """The Transaction created that creates a new Guaranteed Stop Loss Order for the Trade.

    supplemental to v20 API 3.0.25
    """


__all__ = ("SetTradeDependentOrders200Response",)
