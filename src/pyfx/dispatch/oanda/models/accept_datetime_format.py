"""AcceptDatetimeFormat definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum


class AcceptDatetimeFormat(ApiEnum):
    """
    DateTime header
    """

    __finalize__: ClassVar[Literal[True]] = True

    UNIX = 'UNIX'
    RFC3339 = 'RFC3339'


__all__ = ("AcceptDatetimeFormat",)
