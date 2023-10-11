
"""model definition for OANDA v20 REST API (3.0.25)"""




from typing import Optional


from .market_order_reject_transaction import MarketOrderRejectTransaction


from ..transport import ApiObject, TransportField
from ..util import exporting



class ClosePosition400Response(ApiObject):
    """
    ClosePosition400Response
    """
    long_order_reject_transaction: Optional[MarketOrderRejectTransaction] = TransportField(None, alias="longOrderRejectTransaction")
    short_order_reject_transaction: Optional[MarketOrderRejectTransaction] = TransportField(None, alias="shortOrderRejectTransaction")
    
__all__ = exporting(__name__, ...)

