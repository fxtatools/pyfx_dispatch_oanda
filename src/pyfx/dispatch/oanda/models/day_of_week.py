"""DayOfWeek definition for OANDA v20 REST API (3.0.25)"""

from enum import Enum

class DayOfWeek(str, Enum):
    """The DayOfWeek provides a representation of the day of the week.
    """

    SUNDAY = "SUNDAY"
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"

__all__ = ("DayOfWeek",)
