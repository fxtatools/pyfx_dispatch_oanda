"""DayOfWeek definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum

class DayOfWeek(ApiEnum):
    """The DayOfWeek provides a representation of the day of the week.
    """

    __finalize__: ClassVar[Literal[True]] = True

    SUNDAY = "SUNDAY"
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"

__all__ = ("DayOfWeek",)
