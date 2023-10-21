"""GetInstrumentCandles200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField

from .candlestick import Candlestick
from .candlestick_granularity import CandlestickGranularity
from .common_types import InstrumentName

class GetInstrumentCandles200Response(ApiObject):
    """
    GetInstrumentCandles200Response
    """

    instrument: Annotated[InstrumentName, TransportField(...)]
    """The instrument whose Prices are represented by the candlesticks.
    """

    granularity: Annotated[CandlestickGranularity, TransportField(...)]
    """The granularity of the candlesticks provided.
    """

    candles: Annotated[list[Candlestick], TransportField(...)]
    """The list of candlesticks that satisfy the request.
    """


__all__ = ("GetInstrumentCandles200Response",)
