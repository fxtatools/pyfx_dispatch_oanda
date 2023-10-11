
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Optional


from ..transport import ApiObject, TransportField
from ..util import exporting


class MarketOrderTradeClose(ApiObject):
    """
    A MarketOrderTradeClose specifies the extensions to a Market Order that has been created specifically to close a Trade.
    """
    trade_id: Optional[str] = TransportField(None, alias="tradeID")
    """
    The ID of the Trade requested to be closed
    """
    client_trade_id: Optional[str] = TransportField(None, alias="clientTradeID")
    """
    The client ID of the Trade requested to be closed
    """
    units: Optional[str] = TransportField(None)
    """
    Indication of how much of the Trade to close. Either \"ALL\", or a DecimalNumber reflection a partial close of the Trade.
    """


__all__ = exporting(__name__, ...)
