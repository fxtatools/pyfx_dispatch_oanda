
"""model definition for OANDA v20 REST API (3.0.25)"""




from typing import Optional


from .market_order_transaction import MarketOrderTransaction
from .order_cancel_transaction import OrderCancelTransaction
from .order_fill_transaction import OrderFillTransaction


from ..transport import ApiObject, TransportField
from ..util import exporting



class CloseTrade200Response(ApiObject):
    """
    CloseTrade200Response
    """
    order_create_transaction: Optional[MarketOrderTransaction] = TransportField(None, alias="orderCreateTransaction")
    order_fill_transaction: Optional[OrderFillTransaction] = TransportField(None, alias="orderFillTransaction")
    order_cancel_transaction: Optional[OrderCancelTransaction] = TransportField(None, alias="orderCancelTransaction")
    related_transaction_ids: Optional[list[str]] = TransportField(None, alias="relatedTransactionIDs")
    """The IDs of all Transactions that were created while satisfying the request.
    """
    last_transaction_id: Optional[str] = TransportField(None, alias="lastTransactionID")
    """The ID of the most recent Transaction created for the Account
    """


__all__ = exporting(__name__, ...)

