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





class OrderPositionFill(str, Enum):
    """
    Specification of how Positions in the Account are modified when the Order is filled.
    """

    """
    allowed enum values
    """
    OPEN_ONLY = 'OPEN_ONLY'
    REDUCE_FIRST = 'REDUCE_FIRST'
    REDUCE_ONLY = 'REDUCE_ONLY'
    DEFAULT = 'DEFAULT'

    @classmethod
    def from_json(cls, json_str: str) -> OrderPositionFill:
        """Create an instance of OrderPositionFill from a JSON string"""
        return OrderPositionFill(json.loads(json_str))


