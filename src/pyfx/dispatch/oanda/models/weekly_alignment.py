
"""model definition for OANDA v20 REST API (3.0.25)"""


from enum import Enum





from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting



class WeeklyAlignment(str, Enum):
    """
    The day of the week to use for candlestick granularities with weekly alignment.
    """

    """
    allowed enum values
    """
    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'
    SUNDAY = 'Sunday'



__all__ = exporting(__name__, ...)

