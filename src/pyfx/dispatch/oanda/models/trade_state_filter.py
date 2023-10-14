
"""model definition for OANDA v20 REST API (3.0.25)"""


from enum import Enum





from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting



class TradeStateFilter(str, Enum):
    """
    The state to filter the Trades by
    """

    """
    allowed enum values
    """
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    CLOSE_WHEN_TRADEABLE = 'CLOSE_WHEN_TRADEABLE'
    ALL = 'ALL'



__all__ = exporting(__name__, ...)

