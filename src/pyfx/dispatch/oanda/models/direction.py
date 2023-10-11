
"""model definition for OANDA v20 REST API (3.0.25)"""

from enum import Enum

from ..transport import ApiObject, TransportField
from ..util import exporting

class Direction(str, Enum):
    """
    In the context of an Order or a Trade, defines whether the units are positive or negative.
    """

    """
    allowed enum values
    """
    LONG = 'LONG'
    SHORT = 'SHORT'


__all__ = exporting(__name__, ...)
