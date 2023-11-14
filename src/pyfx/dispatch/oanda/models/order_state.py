
"""OrderState definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum

class OrderState(ApiEnum):
    """
    The current state of the Order.
    """


    __finalize__: ClassVar[Literal[True]] = True

    PENDING = 'PENDING'
    FILLED = 'FILLED'
    TRIGGERED = 'TRIGGERED'
    CANCELLED = 'CANCELLED'


__all__ = ("OrderState",)
