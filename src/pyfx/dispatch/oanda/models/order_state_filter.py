
"""model definition for OANDA v20 REST API (3.0.25)"""


from enum import Enum


from ..transport import ApiObject, TransportField
from ..util import exporting


class OrderStateFilter(str, Enum):
    """
    The state to filter the requested Orders by.
    """

    """
    allowed enum values
    """
    PENDING = 'PENDING'
    FILLED = 'FILLED'
    TRIGGERED = 'TRIGGERED'
    CANCELLED = 'CANCELLED'
    ALL = 'ALL'


__all__ = exporting(__name__, ...)
