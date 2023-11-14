
"""StopLossOrderReason definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum


class StopLossOrderReason(ApiEnum):
    """
    The reason that the Stop Loss Order was initiated
    """


    __finalize__: ClassVar[Literal[True]] = True

    CLIENT_ORDER = 'CLIENT_ORDER'
    REPLACEMENT = 'REPLACEMENT'
    ON_FILL = 'ON_FILL'


__all__ = ("StopLossOrderReason",)
