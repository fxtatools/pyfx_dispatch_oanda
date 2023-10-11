
"""AcceptDatetimeFormat definition for OANDA v20 REST API (3.0.25)"""

from enum import Enum

from ..util import exporting


class AcceptDatetimeFormat(str, Enum):
    """
    DateTime header
    """

    """
    allowed enum values
    """
    UNIX = 'UNIX'
    RFC3339 = 'RFC3339'


__all__ = ("AcceptDatetimeFormat",)
