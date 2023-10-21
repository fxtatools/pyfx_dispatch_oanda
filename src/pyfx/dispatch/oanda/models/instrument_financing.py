"""InstrumentFinancing model definition"""

from typing import Annotated, Optional

from .financing_days_of_week import FinancingDaysOfWeek
from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from .common_types import FloatValue


class InstrumentFinancing(ApiObject):
    """
    Financing data for the instrument

    supplemental to v20 3.0.25
    """

    long_rate: Annotated[Optional[FloatValue], TransportField(None, alias="longRate")]
    """
    The financing rate to be used for a long position for the instrument. The value is in decimal rather than percentage points, i.e. 5% is represented 0.05.
    """

    short_rate: Annotated[Optional[FloatValue], TransportField(None, alias="shortRate")]
    """
    The financing rate to be used for a short position for the instrument. The value is in decimal rather than percentage points, i.e. 5% is represented as 0.05.
    """

    financing_days_of_week: Annotated[Optional[list[FinancingDaysOfWeek]], TransportField(None, alias="financingDaysOfWeek")]
    """
    The days of the week to debit or credit financing charges; the exact time of day at which to charge the financing is set in the DivisionTradingGroup for the client's account.
    """


__all__ = ("InstrumentFinancing",)
