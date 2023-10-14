
"""TradeState definition for OANDA v20 REST API (3.0.25)"""

from enum import Enum

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting


class TradeState(str, Enum):
    """
    The current state of the Trade, one of OPEN, CLOSED, or CLOSE_WHEN_TRADEABLE
    """

    """
    allowed enum values
    """
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    CLOSE_WHEN_TRADEABLE = 'CLOSE_WHEN_TRADEABLE'


__all__ = exporting(__name__, ...)

