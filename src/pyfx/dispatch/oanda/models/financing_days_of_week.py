"""FinancingDaysOfWeek model definition"""

from typing import Annotated, Optional

from ..transport import ApiObject, TransportField

from .day_of_week import DayOfWeek


class FinancingDaysOfWeek(ApiObject):
    """
    A FinancingDayOfWeek message defines a day of the week when financing charges are debited or credited.

    supplemental to v20 3.0.25
    """

    day_of_week: Annotated[Optional[DayOfWeek], TransportField(None, alias="dayOfWeek")]
    """
    The day of the week to charge the financing.
    """

    days_charged: Annotated[Optional[int], TransportField(None, alias="daysCharged")]
    """
    The number of days worth of financing to be charged on dayOfWeek.
    """


__all__ = ("FinancingDaysOfWeek",)
