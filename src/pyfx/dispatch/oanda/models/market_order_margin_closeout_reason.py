
"""model definition for OANDA v20 REST API (3.0.25)"""


from enum import Enum


from ..transport import ApiObject, TransportField
from ..util import exporting


class MarketOrderMarginCloseoutReason(str, Enum):
    """
    The reason that the Market Order was created to perform a margin closeout
    """

    """
    allowed enum values
    """
    MARGIN_CHECK_VIOLATION = 'MARGIN_CHECK_VIOLATION'
    REGULATORY_MARGIN_CALL_VIOLATION = 'REGULATORY_MARGIN_CALL_VIOLATION'
    REGULATORY_MARGIN_CHECK_VIOLATION = 'REGULATORY_MARGIN_CHECK_VIOLATION'


__all__ = exporting(__name__, ...)
