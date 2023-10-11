
"""model definition for OANDA v20 REST API (3.0.25)"""




from typing import Optional


from .market_order_transaction import MarketOrderTransaction
from .order_cancel_transaction import OrderCancelTransaction
from .order_fill_transaction import OrderFillTransaction


from ..transport import ApiObject, TransportField
from ..util import exporting



class ClosePosition200Response(ApiObject):
    """
    ClosePosition200Response
    """
    long_order_create_transaction: Optional[MarketOrderTransaction] = TransportField(None, alias="longOrderCreateTransaction")
    long_order_fill_transaction: Optional[OrderFillTransaction] = TransportField(None, alias="longOrderFillTransaction")
    long_order_cancel_transaction: Optional[OrderCancelTransaction] = TransportField(None, alias="longOrderCancelTransaction")
    short_order_create_transaction: Optional[MarketOrderTransaction] = TransportField(None, alias="shortOrderCreateTransaction")
    short_order_fill_transaction: Optional[OrderFillTransaction] = TransportField(None, alias="shortOrderFillTransaction")
    short_order_cancel_transaction: Optional[OrderCancelTransaction] = TransportField(None, alias="shortOrderCancelTransaction")
    related_transaction_ids: Optional[list[str]] = TransportField(None, alias="relatedTransactionIDs")
    """The IDs of all Transactions that were created while satisfying the request.
    """
    last_transaction_id: Optional[str] = TransportField(None, alias="lastTransactionID")
    """The ID of the most recent Transaction created for the Account
    """


__all__ = exporting(__name__, ...)

