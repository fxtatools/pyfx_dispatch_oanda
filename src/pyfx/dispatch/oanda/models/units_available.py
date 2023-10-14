
"""model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from .units_available_details import UnitsAvailableDetails

from ..transport import ApiObject, TransportField
from ..util import exporting


class UnitsAvailable(ApiObject):
    """
    Representation of how many units of an Instrument are available to be traded by an Order depending on its postionFill option.
    
    [Deprecated, see usage in ClientPrice]
    """
    default: Annotated[Optional[UnitsAvailableDetails], TransportField(None)]
    """
    The number of units that are available to be traded using an Order with a positionFill option of “DEFAULT”. For an Account with hedging enabled, this value will be the same as the “OPEN_ONLY” value. For an Account without hedging enabled, this value will be the same as the “REDUCE_FIRST” value.
    """
    reduce_first: Annotated[Optional[UnitsAvailableDetails], TransportField(None, alias="reduceFirst")]
    reduce_only: Annotated[Optional[UnitsAvailableDetails], TransportField(None, alias="reduceOnly")]
    open_only: Annotated[Optional[UnitsAvailableDetails], TransportField(None, alias="openOnly")]


__all__ = exporting(__name__, ...)
