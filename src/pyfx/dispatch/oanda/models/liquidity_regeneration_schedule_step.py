"""LiquidityRegenerationScheduleStep model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField

from .common_types import Time, FloatValue


class LiquidityRegenerationScheduleStep(ApiObject):
    """
    A liquidity regeneration schedule Step indicates the amount of bid and ask liquidity that is used by the Account
    at a certain time.

    These amounts will only change at the timestamp of the following step.
    """

    timestamp: Annotated[Time, TransportField(...)]
    """
    The timestamp of the schedule step.
    """

    bid_liquidity_used: Annotated[Optional[FloatValue], TransportField(None, alias="bidLiquidityUsed")]
    """
    The amount of bid liquidity used at this step in the schedule.
    """

    ask_liquidity_used: Annotated[Optional[FloatValue], TransportField(None, alias="askLiquidityUsed")]
    """
    The amount of ask liquidity used at this step in the schedule.
    """


__all__ = ("LiquidityRegenerationScheduleStep",)
