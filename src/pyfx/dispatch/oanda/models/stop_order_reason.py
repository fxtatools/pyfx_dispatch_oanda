
"""StopOrderReason definition for OANDA v20 REST API (3.0.25)"""


from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum


class StopOrderReason(ApiEnum):
    """
    The reason that the Stop Order was initiated
    """


    __finalize__: ClassVar[Literal[True]] = True

    CLIENT_ORDER = 'CLIENT_ORDER'
    REPLACEMENT = 'REPLACEMENT'


__all__ = ("StopOrderReason",)
