
"""model definition for OANDA v20 REST API (3.0.25)"""

## e.g usage in streaming response during weekend hours
##  {"type":"PRICE","time":"2023-09-29T20:58:00.136640494Z","bids":[{"price":"0.86582","liquidity":10000000}],"asks":[{"price":"0.86704","liquidity":10000000}],"closeoutBid":"0.86582","closeoutAsk":"0.86704","status":"non-tradeable","tradeable":false,"instrument":"EUR_GBP"}
## ... once for each requested instrument, then followed by heartbeat responses ... until tradeable 

from enum import Enum

from ..util import exporting

class PriceStatus(str, Enum):
    """
    The status of the Price.
    """

    """
    allowed enum values
    """
    TRADEABLE = 'tradeable'
    NON_TRADEABLE = 'non-tradeable'
    INVALID = 'invalid'


__all__ = exporting(__name__, ...)
