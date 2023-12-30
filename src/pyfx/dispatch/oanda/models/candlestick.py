"""Candlestick model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

import numpy as np

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField

from .candlestick_data import CandlestickData
from .common_types import Time


class Candlestick(ApiObject):
    """
    The Candlestick representation
    """

    time: Annotated[Time, TransportField(...)]
    """
    The start time of the candlestick
    """

    ask: Annotated[Optional[CandlestickData], TransportField(None)]
    """
    The candlestick data based on asks. Only provided if ask-based candles were requested.
    """

    mid: Annotated[Optional[CandlestickData], TransportField(None)]
    """
    The candlestick data based on median of ask and bid. Only provided if midpoint-based candles were requested.
    """

    bid: Annotated[Optional[CandlestickData], TransportField(None)]
    """
    The candlestick data based on bids. Only provided if bid-based candles were requested.
    """

    volume: Annotated[int, TransportField(..., storage_type = np.uint32)]
    """
    The number of prices created during the time-range represented by the candlestick.
    """

    complete: Annotated[Optional[bool], TransportField(None)]
    """
    A flag indicating if the candlestick is complete. A complete candlestick is one whose ending time is not in the future.
    """


__all__ = ("Candlestick",)
