
"""model definition for OANDA v20 REST API (3.0.25)"""




from typing import Optional


from .market_order_reject_transaction import MarketOrderRejectTransaction

from ..transport import ApiObject, TransportField
from ..util import exporting



class CloseTrade400Response(ApiObject):
    """
    CloseTrade400Response
    """
    order_reject_transaction: Optional[MarketOrderRejectTransaction] = TransportField(None, alias="orderRejectTransaction")
    error_code: Optional[str] = TransportField(None, alias="errorCode")
    """The code of the error that has occurred. This field may not be returned for some errors.
    """
    error_message: Optional[str] = TransportField(None, alias="errorMessage")
    """The human-readable description of the error that has occurred.
    """


__all__ = exporting(__name__, ...)

