
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Optional


from ..transport import ApiObject, TransportField
from ..util import exporting


class GuaranteedStopLossOrderLevelRestriction(ApiObject):
    """
    A GuaranteedStopLossOrderLevelRestriction represents the total position size that can exist within a given price window for Trades with guaranteed Stop Loss Orders attached for a specific Instrument.
    """
    volume: Optional[str] = TransportField(None)
    """
    Applies to Trades with a guaranteed Stop Loss Order attached for the specified Instrument. This is the total allowed Trade volume that can exist within the priceRange based on the trigger prices of the guaranteed Stop Loss Orders.
    """
    price_range: Optional[str] = TransportField(None, alias="priceRange")
    """
    The price range the volume applies to. This value is in price units.
    """


__all__ = exporting(__name__, ...)
