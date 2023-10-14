
"""UnitsAvailableDetails model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting
from .common_types import LotsValue


class UnitsAvailableDetails(ApiObject):
    """
    Representation of many units of an Instrument are available to be traded for both long and short Orders.
    """

    long: Annotated[Optional[LotsValue], TransportField(None)]
    """
    The units available for long Orders.
    """

    short: Annotated[Optional[LotsValue], TransportField(None)]
    """
    The units available for short Orders.
    """


__all__ = ("UnitsAvailableDetails",)
