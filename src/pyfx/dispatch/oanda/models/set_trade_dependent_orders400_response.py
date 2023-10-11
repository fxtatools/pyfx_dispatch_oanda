
"""model definition for OANDA v20 REST API (3.0.25)"""




from typing import Optional


from .order_cancel_reject_transaction import OrderCancelRejectTransaction
from .stop_loss_order_reject_transaction import StopLossOrderRejectTransaction
from .take_profit_order_reject_transaction import TakeProfitOrderRejectTransaction
from .trailing_stop_loss_order_reject_transaction import TrailingStopLossOrderRejectTransaction


from ..transport import ApiObject, TransportField
from ..util import exporting



class SetTradeDependentOrders400Response(ApiObject):
    """
    SetTradeDependentOrders400Response
    """
    take_profit_order_cancel_reject_transaction: Optional[OrderCancelRejectTransaction] = TransportField(None, alias="takeProfitOrderCancelRejectTransaction")
    take_profit_order_reject_transaction: Optional[TakeProfitOrderRejectTransaction] = TransportField(None, alias="takeProfitOrderRejectTransaction")
    stop_loss_order_cancel_reject_transaction: Optional[OrderCancelRejectTransaction] = TransportField(None, alias="stopLossOrderCancelRejectTransaction")
    stop_loss_order_reject_transaction: Optional[StopLossOrderRejectTransaction] = TransportField(None, alias="stopLossOrderRejectTransaction")
    trailing_stop_loss_order_cancel_reject_transaction: Optional[OrderCancelRejectTransaction] = TransportField(None, alias="trailingStopLossOrderCancelRejectTransaction")
    trailing_stop_loss_order_reject_transaction: Optional[TrailingStopLossOrderRejectTransaction] = TransportField(None, alias="trailingStopLossOrderRejectTransaction")
    last_transaction_id: Optional[str] = TransportField(None, alias="lastTransactionID")
    """
    The ID of the most recent Transaction created for the Account.
    """
    related_transaction_ids: Optional[list[str]] = TransportField(None, alias="relatedTransactionIDs")
    """
    The IDs of all Transactions that were created while satisfying the request.
    """
    error_code: Optional[str] = TransportField(None, alias="errorCode")
    """
    The code of the error that has occurred. This field may not be returned for some errors.
    """
    error_message: Optional[str] = TransportField(None, alias="errorMessage")
    """
    The human-readable description of the error that has occurred.
    """


__all__ = exporting(__name__, ...)

