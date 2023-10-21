"""PositionAggregationMode definition for OANDA v20 REST API (3.0.25)"""

from enum import Enum


class PositionAggregationMode(str, Enum):
    """
    The way that position values for an Account are calculated and aggregated.
    """

    ABSOLUTE_SUM = 'ABSOLUTE_SUM'
    MAXIMAL_SIDE = 'MAXIMAL_SIDE'
    NET_SUM = 'NET_SUM'


__all__ = ("PositionAggregationMode",)
