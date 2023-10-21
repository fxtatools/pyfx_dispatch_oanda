"""GuaranteedStopLossOrderLevelRestriction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from .common_types import PriceValue, FloatValue


class GuaranteedStopLossOrderLevelRestriction(ApiObject):
    """
    A GuaranteedStopLossOrderLevelRestriction represents the total position size that can exist within a
    given price window for Trades with guaranteed Stop Loss Orders attached for a specific Instrument.
    """

    volume: Annotated[Optional[FloatValue], TransportField(None)]
    """
    Applies to Trades with a guaranteed Stop Loss Order attached for the specified Instrument.

    This is the total allowed Trade volume that can exist within the priceRange based on the trigger prices
    of the guaranteed Stop Loss Orders.
    """

    price_range: Annotated[Optional[PriceValue], TransportField(None, alias="priceRange")]
    """
    The price range the volume applies to. This value is in price units.
    """


__all__ = ("GuaranteedStopLossOrderLevelRestriction",)
