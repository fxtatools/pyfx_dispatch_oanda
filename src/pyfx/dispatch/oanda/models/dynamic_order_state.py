
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Annotated, Optional


from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting

from .common_types import PriceValue

class DynamicOrderState(ApiObject):
    """
    The dynamic state of an Order. This is only relevant to TrailingStopLoss Orders, as no other Order type has dynamic state.
    """
    id: Annotated[Optional[str], TransportField(None)]
    """The Order's ID.
    """
    trailing_stop_value: Annotated[Optional[str], TransportField(None, alias="trailingStopValue")]
    """The Order's calculated trailing stop value.
    """
    trigger_distance: Annotated[Optional[PriceValue], TransportField(None, alias="triggerDistance")]
    """The distance between the Trailing Stop Loss Order's trailingStopValue and the current Market Price. This represents the distance (in price units) of the Order from a triggering price. If the distance could not be determined, this value will not be set.
    """
    is_trigger_distance_exact: Annotated[Optional[bool], TransportField(None, alias="isTriggerDistanceExact")]
    """True if an exact trigger distance could be calculated. If false, it means the provided trigger distance is a best estimate. If the distance could not be determined, this value will not be set.
    """


__all__ = exporting(__name__, ...)
