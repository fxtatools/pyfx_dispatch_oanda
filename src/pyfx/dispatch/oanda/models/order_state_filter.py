"""OrderStateFilter definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum


class OrderStateFilter(ApiEnum):
    """
    The state to filter the requested Orders by.
    """


    __finalize__: ClassVar[Literal[True]] = True

    PENDING = 'PENDING'
    FILLED = 'FILLED'
    TRIGGERED = 'TRIGGERED'
    CANCELLED = 'CANCELLED'
    ALL = 'ALL'


__all__ = ("OrderStateFilter",)
