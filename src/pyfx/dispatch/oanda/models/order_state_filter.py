"""OrderStateFilter definition for OANDA v20 REST API (3.0.25)"""

from enum import Enum


class OrderStateFilter(str, Enum):
    """
    The state to filter the requested Orders by.
    """

    PENDING = 'PENDING'
    FILLED = 'FILLED'
    TRIGGERED = 'TRIGGERED'
    CANCELLED = 'CANCELLED'
    ALL = 'ALL'


__all__ = ("OrderStateFilter",)
