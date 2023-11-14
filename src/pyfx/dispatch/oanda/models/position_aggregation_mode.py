"""PositionAggregationMode definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum


class PositionAggregationMode(ApiEnum):
    """
    The way that position values for an Account are calculated and aggregated.
    """


    __finalize__: ClassVar[Literal[True]] = True

    ABSOLUTE_SUM = 'ABSOLUTE_SUM'
    MAXIMAL_SIDE = 'MAXIMAL_SIDE'
    NET_SUM = 'NET_SUM'


__all__ = ("PositionAggregationMode",)
