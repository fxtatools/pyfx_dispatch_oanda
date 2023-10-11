
"""model definition for OANDA v20 REST API (3.0.25)"""

from pandas import Timestamp
from typing import Optional

from ..transport import ApiObject, TransportField
from ..util import exporting


class LiquidityRegenerationScheduleStep(ApiObject):
    """
    A liquidity regeneration schedule Step indicates the amount of bid and ask liquidity that is used by the Account at a certain time. These amounts will only change at the timestamp of the following step.
    """
    timestamp: Optional[Timestamp] = TransportField(None)
    """
    The timestamp of the schedule step.
    """
    bid_liquidity_used: Optional[str] = TransportField(None, alias="bidLiquidityUsed")
    """
    The amount of bid liquidity used at this step in the schedule.
    """
    ask_liquidity_used: Optional[str] = TransportField(None, alias="askLiquidityUsed")
    """
    The amount of ask liquidity used at this step in the schedule.
    """


__all__ = exporting(__name__, ...)
