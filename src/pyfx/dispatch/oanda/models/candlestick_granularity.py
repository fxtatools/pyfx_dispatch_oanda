# coding: utf-8

"""
    OANDA v20 REST API

    The full OANDA v20 REST API Specification. This specification defines how to interact with v20 Accounts, Trades, Orders, Pricing and more.

    The version of the OpenAPI document: 3.0.25

    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import json
import pprint
import re  # noqa: F401
from aenum import Enum, no_arg





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

    @classmethod
    def from_json(cls, json_str: str) -> "CandlestickGranularity":
        """Create an instance of CandlestickGranularity from a JSON string"""
        return CandlestickGranularity(json.loads(json_str))


