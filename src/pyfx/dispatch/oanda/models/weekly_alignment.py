"""WeeklyAlignment definition for OANDA v20 REST API (3.0.25)"""

from enum import Enum


class WeeklyAlignment(str, Enum):
    """
    The day of the week to use for candlestick granularities with weekly alignment.
    """

    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'
    SUNDAY = 'Sunday'



__all__ = ("WeeklyAlignment",)
