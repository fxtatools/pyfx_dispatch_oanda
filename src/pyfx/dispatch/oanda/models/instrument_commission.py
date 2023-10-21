"""InstrumentCommission model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField

from .common_types import FloatValue


class InstrumentCommission(ApiObject):
    """
    An InstrumentCommission represents an instrument-specific commission
    """

    commission: Annotated[Optional[FloatValue], TransportField(None)]
    """
    The commission amount (in the Account's home currency) charged per unitsTraded of the instrument
    """

    units_traded: Annotated[Optional[FloatValue], TransportField(None, alias="unitsTraded")]
    """
    The number of units traded that the commission amount is based on.
    """

    minimum_commission: Annotated[Optional[FloatValue], TransportField(None, alias="minimumCommission")]
    """
    The minimum commission amount (in the Account's home currency) that is charged when an Order is filled for this instrument.
    """


__all__ = ("InstrumentCommission",)
