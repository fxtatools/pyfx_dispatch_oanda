
"""OrderState definition for OANDA v20 REST API (3.0.25)"""

from enum import Enum

class OrderState(str, Enum):
    """
    The current state of the Order.
    """

    PENDING = 'PENDING'
    FILLED = 'FILLED'
    TRIGGERED = 'TRIGGERED'
    CANCELLED = 'CANCELLED'


__all__ = ("OrderState",)
