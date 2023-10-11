
"""model definition for OANDA v20 REST API (3.0.25)"""

from enum import Enum

from ..util import exporting


class GuaranteedStopLossOrderMode(str, Enum):
    """
    The overall behaviour of the Account regarding guaranteed Stop Loss Orders.
    """

    """
    allowed enum values
    """
    DISABLED = 'DISABLED'
    ALLOWED = 'ALLOWED'
    REQUIRED = 'REQUIRED'


__all__ = exporting(__name__, ...)
