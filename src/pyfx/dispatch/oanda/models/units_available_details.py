
"""UnitsAvailableDetails model definition for OANDA v20 REST API (3.0.25)"""

from typing import Optional

from ..transport import ApiObject, TransportField
from ..util import exporting
from .common_types import LotsValue


class UnitsAvailableDetails(ApiObject):
    """
    Representation of many units of an Instrument are available to be traded for both long and short Orders.
    """

    long: Optional[LotsValue] = TransportField(None)
    """
    The units available for long Orders.
    """

    short: Optional[LotsValue] = TransportField(None)
    """
    The units available for short Orders.
    """


__all__ = ("UnitsAvailableDetails",)
