from enum import Enum

class DayOfWeek(str, Enum):
    """The DayOfWeek provides a representation of the day of the week.

    supplemental to v20 3.0.25"""
    Sunday = "SUNDAY"
    Monday = "MONDAY"
    Tuesday = "TUESDAY"
    Wednesday = "WEDNESDAY"
    Thursday = "THURSDAY"
    Friday = "FRIDAY"
    Saturday = "SATURDAY"

__all__ = ("DayOfWeek",)
