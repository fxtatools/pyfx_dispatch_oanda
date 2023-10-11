
"""model definition for OANDA v20 REST API (3.0.25)"""




from typing import Optional


from .order_cancel_transaction import OrderCancelTransaction
from .order_fill_transaction import OrderFillTransaction
from .transaction import Transaction
from .response_mixins import TransactionResponse


from ..transport import ApiObject, TransportField
from ..util import exporting



class CreateOrder201Response(ApiObject):
    """
    CreateOrder201Response
    """
    order_create_transaction: Optional[Transaction] = TransportField(None, alias="orderCreateTransaction")
    order_fill_transaction: Optional[OrderFillTransaction] = TransportField(None, alias="orderFillTransaction")
    order_cancel_transaction: Optional[OrderCancelTransaction] = TransportField(None, alias="orderCancelTransaction")
    order_reissue_transaction: Optional[Transaction] = TransportField(None, alias="orderReissueTransaction")
    order_reissue_reject_transaction: Optional[Transaction] = TransportField(None, alias="orderReissueRejectTransaction")
    related_transaction_ids: Optional[list[str]] = TransportField(None, alias="relatedTransactionIDs")
    """The IDs of all Transactions that were created while satisfying the request.
    """
    last_transaction_id: Optional[str] = TransportField(None, alias="lastTransactionID")
    """The ID of the most recent Transaction created for the Account
    """


__all__ = exporting(__name__, ...)

