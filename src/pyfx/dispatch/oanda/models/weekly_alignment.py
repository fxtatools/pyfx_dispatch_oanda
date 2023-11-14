"""WeeklyAlignment definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum


class WeeklyAlignment(ApiEnum):
    """
    The day of the week to use for candlestick granularities with weekly alignment.
    """


    __finalize__: ClassVar[Literal[True]] = True

    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'
    SUNDAY = 'Sunday'



__all__ = ("WeeklyAlignment",)
