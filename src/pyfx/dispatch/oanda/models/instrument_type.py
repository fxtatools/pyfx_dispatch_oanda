
"""model definition for OANDA v20 REST API (3.0.25)"""


from enum import Enum


from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting


class InstrumentType(str, Enum):
    """
    The type of an Instrument.
    """

    """
    allowed enum values
    """
    CURRENCY = 'CURRENCY'
    CFD = 'CFD'
    METAL = 'METAL'


__all__ = exporting(__name__, ...)
