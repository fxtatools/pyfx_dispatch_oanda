
"""model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from .liquidity_regeneration_schedule_step import LiquidityRegenerationScheduleStep

from ..transport import ApiObject, TransportField
from ..util import exporting


class LiquidityRegenerationSchedule(ApiObject):
    """
    A LiquidityRegenerationSchedule indicates how liquidity that is used when filling an Order for an instrument is regenerated following the fill.  A liquidity regeneration schedule will be in effect until the timestamp of its final step, but may be replaced by a schedule created for an Order of the same instrument that is filled while it is still in effect.
    """
    steps: Annotated[Optional[list[LiquidityRegenerationScheduleStep]], TransportField(None)]
    """
    The steps in the Liquidity Regeneration Schedule
    """


__all__ = exporting(__name__, ...)
