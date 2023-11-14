
"""OrderPositionFill definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum


class OrderPositionFill(ApiEnum):
    """
    Specification of how Positions in the Account are modified when the Order is filled.
    """


    __finalize__: ClassVar[Literal[True]] = True

    OPEN_ONLY = 'OPEN_ONLY'
    REDUCE_FIRST = 'REDUCE_FIRST'
    REDUCE_ONLY = 'REDUCE_ONLY'
    DEFAULT = 'DEFAULT'


__all__ = ("OrderPositionFill",)
