
"""CandlestickGranularity definition for OANDA v20 REST API (3.0.25)"""

from enum import Enum


class CandlestickGranularity(str, Enum):
    """
    The granularity of a candlestick
    """

    """
    allowed enum values
    """
    S5 = 'S5'
    S10 = 'S10'
    S15 = 'S15'
    S30 = 'S30'
    M1 = 'M1'
    M2 = 'M2'
    M4 = 'M4'
    M5 = 'M5'
    M10 = 'M10'
    M15 = 'M15'
    M30 = 'M30'
    H1 = 'H1'
    H2 = 'H2'
    H3 = 'H3'
    H4 = 'H4'
    H6 = 'H6'
    H8 = 'H8'
    H12 = 'H12'
    D = 'D'
    W = 'W'
    M = 'M'


__all__ = ("CandlestickGranularity",)
