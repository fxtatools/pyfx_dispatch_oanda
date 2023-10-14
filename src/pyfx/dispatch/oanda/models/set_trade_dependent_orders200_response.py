
"""model definition for OANDA v20 REST API (3.0.25)"""




from typing import Annotated, Optional


from .order_cancel_transaction import OrderCancelTransaction
from .order_fill_transaction import OrderFillTransaction
from .stop_loss_order_transaction import StopLossOrderTransaction
from .take_profit_order_transaction import TakeProfitOrderTransaction
from .trailing_stop_loss_order_transaction import TrailingStopLossOrderTransaction


from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting



class SetTradeDependentOrders200Response(ApiObject):
    """
    SetTradeDependentOrders200Response
    """
    take_profit_order_cancel_transaction: Annotated[Optional[OrderCancelTransaction], TransportField(None, alias="takeProfitOrderCancelTransaction")]
    take_profit_order_transaction: Annotated[Optional[TakeProfitOrderTransaction], TransportField(None, alias="takeProfitOrderTransaction")]
    take_profit_order_fill_transaction: Annotated[Optional[OrderFillTransaction], TransportField(None, alias="takeProfitOrderFillTransaction")]
    take_profit_order_created_cancel_transaction: Annotated[Optional[OrderCancelTransaction], TransportField(None, alias="takeProfitOrderCreatedCancelTransaction")]
    stop_loss_order_cancel_transaction: Annotated[Optional[OrderCancelTransaction], TransportField(None, alias="stopLossOrderCancelTransaction")]
    stop_loss_order_transaction: Annotated[Optional[StopLossOrderTransaction], TransportField(None, alias="stopLossOrderTransaction")]
    stop_loss_order_fill_transaction: Annotated[Optional[OrderFillTransaction], TransportField(None, alias="stopLossOrderFillTransaction")]
    stop_loss_order_created_cancel_transaction: Annotated[Optional[OrderCancelTransaction], TransportField(None, alias="stopLossOrderCreatedCancelTransaction")]
    trailing_stop_loss_order_cancel_transaction: Annotated[Optional[OrderCancelTransaction], TransportField(None, alias="trailingStopLossOrderCancelTransaction")]
    trailing_stop_loss_order_transaction: Annotated[Optional[TrailingStopLossOrderTransaction], TransportField(None, alias="trailingStopLossOrderTransaction")]
    related_transaction_ids: Annotated[Optional[list[str]], TransportField(None, alias="relatedTransactionIDs")]
    """
    The IDs of all Transactions that were created while satisfying the request.
    """
    last_transaction_id: Annotated[Optional[str], TransportField(None, alias="lastTransactionID")]
    """
    The ID of the most recent Transaction created for the Account
    """


__all__ = exporting(__name__, ...)

