"""Direction definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum


class Direction(ApiEnum):
    """
    In the context of an Order or a Trade, defines whether the units are positive or negative.
    """


    __finalize__: ClassVar[Literal[True]] = True

    LONG = 'LONG'
    SHORT = 'SHORT'


__all__ = ("Direction",)
