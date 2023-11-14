"""TradePL definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum


class TradePL(ApiEnum):
    """
    The classification of TradePLs.
    """


    __finalize__: ClassVar[Literal[True]] = True

    POSITIVE = 'POSITIVE'
    NEGATIVE = 'NEGATIVE'
    ZERO = 'ZERO'


__all__ = ("TradePL",)
