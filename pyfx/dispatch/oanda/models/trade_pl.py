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





class TradePL(str, Enum):
    """
    The classification of TradePLs.
    """

    """
    allowed enum values
    """
    POSITIVE = 'POSITIVE'
    NEGATIVE = 'NEGATIVE'
    ZERO = 'ZERO'

    @classmethod
    def from_json(cls, json_str: str) -> TradePL:
        """Create an instance of TradePL from a JSON string"""
        return TradePL(json.loads(json_str))


