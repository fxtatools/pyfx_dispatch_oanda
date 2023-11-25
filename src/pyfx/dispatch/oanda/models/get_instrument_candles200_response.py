"""GetInstrumentCandles200Response model definition for OANDA v20 REST API (3.0.25)"""

import numpy as np
import pandas as pd
from typing import Annotated

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField

from .candlestick import Candlestick
from .candlestick_granularity import CandlestickGranularity, CandlestickPeriod
from .common_types import InstrumentName, PriceValue, Time

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
