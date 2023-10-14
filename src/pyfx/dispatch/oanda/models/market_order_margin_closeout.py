
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Annotated, Optional


from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting


from .market_order_margin_closeout_reason import MarketOrderMarginCloseoutReason


class MarketOrderMarginCloseout(ApiObject):
    """
    Details for the Market Order extensions specific to a Market Order placed that is part of a Market Order Margin Closeout in a client's account
    """
    reason: Annotated[Optional[MarketOrderMarginCloseoutReason], TransportField(None)]
    """
    The reason the Market Order was created to perform a margin closeout
    """


__all__ = exporting(__name__, ...)
