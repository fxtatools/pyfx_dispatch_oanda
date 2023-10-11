
"""model definition for OANDA v20 REST API (3.0.25)"""


from enum import Enum





from ..transport import ApiObject, TransportField
from ..util import exporting



class TradePL(str, Enum):
    """
    The classification of TradePLs.
    """

    """
    allowed enum values
    """
    POSITIVE = 'POSITIVE'
    NEGATIVE = 'NEGATIVE'
    ZERO = 'ZERO'



__all__ = exporting(__name__, ...)

