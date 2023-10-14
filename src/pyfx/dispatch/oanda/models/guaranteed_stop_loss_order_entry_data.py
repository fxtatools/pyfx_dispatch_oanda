
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Annotated, Optional


from .guaranteed_stop_loss_order_level_restriction import GuaranteedStopLossOrderLevelRestriction

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting

from .common_types import PriceValue

class GuaranteedStopLossOrderEntryData(ApiObject):
    """
    Details required by clients creating a Guaranteed Stop Loss Order
    """
    minimum_distance: Annotated[Optional[PriceValue], TransportField(None, alias="minimumDistance")]
    """
    The minimum distance allowed between the Trade's fill price and the configured price for guaranteed Stop Loss Orders created for this instrument. Specified in price units.
    """
    premium: Annotated[Optional[str], TransportField(None)]
    """
    The amount that is charged to the account if a guaranteed Stop Loss Order is triggered and filled. The value is in price units and is charged for each unit of the Trade.
    """
    level_restriction: Annotated[Optional[GuaranteedStopLossOrderLevelRestriction], TransportField(None, alias="levelRestriction")]


__all__ = exporting(__name__, ...)
