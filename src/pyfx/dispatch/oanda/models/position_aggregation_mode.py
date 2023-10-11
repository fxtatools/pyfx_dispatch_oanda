
"""model definition for OANDA v20 REST API (3.0.25)"""


from enum import Enum


from ..transport import ApiObject, TransportField
from ..util import exporting


class PositionAggregationMode(str, Enum):
    """
    The way that position values for an Account are calculated and aggregated.
    """

    """
    allowed enum values
    """
    ABSOLUTE_SUM = 'ABSOLUTE_SUM'
    MAXIMAL_SIDE = 'MAXIMAL_SIDE'
    NET_SUM = 'NET_SUM'


__all__ = exporting(__name__, ...)
