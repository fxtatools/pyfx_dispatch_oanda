
"""model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport import ApiObject, TransportField

from ..util import exporting

from .candlestick import Candlestick
from .candlestick_granularity import CandlestickGranularity

class GetInstrumentCandles200Response(ApiObject):
    """
    GetInstrumentCandles200Response
    """
    instrument: Annotated[str, TransportField(...)]
    """The instrument whose Prices are represented by the candlesticks.
    """
    granularity: Annotated[CandlestickGranularity, TransportField(...)]
    """The granularity of the candlesticks provided.
    """
    candles: Annotated[list[Candlestick], TransportField(...)]
    """The list of candlesticks that satisfy the request.
    """


__all__ = exporting(__name__, ...)

