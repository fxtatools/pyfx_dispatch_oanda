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





class CancellableOrderType(str, Enum):
    """
    The type of the Order.
    """

    """
    allowed enum values
    """
    LIMIT = 'LIMIT'
    STOP = 'STOP'
    MARKET_IF_TOUCHED = 'MARKET_IF_TOUCHED'
    TAKE_PROFIT = 'TAKE_PROFIT'
    STOP_LOSS = 'STOP_LOSS'
    TRAILING_STOP_LOSS = 'TRAILING_STOP_LOSS'

    @classmethod
    def from_json(cls, json_str: str) -> CancellableOrderType:
        """Create an instance of CancellableOrderType from a JSON string"""
        return CancellableOrderType(json.loads(json_str))

