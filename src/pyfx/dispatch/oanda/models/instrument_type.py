"""InstrumentType definition for OANDA v20 REST API (3.0.25)"""

from enum import Enum


class InstrumentType(str, Enum):
    """
    The type of an Instrument.
    """

    CURRENCY = 'CURRENCY'
    CFD = 'CFD'
    METAL = 'METAL'


__all__ = ("InstrumentType",)
