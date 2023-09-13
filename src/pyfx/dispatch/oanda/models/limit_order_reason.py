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





class LimitOrderReason(str, Enum):
    """
    The reason that the Limit Order was initiated
    """

    """
    allowed enum values
    """
    CLIENT_ORDER = 'CLIENT_ORDER'
    REPLACEMENT = 'REPLACEMENT'

    @classmethod
    def from_json(cls, json_str: str) -> "LimitOrderReason":
        """Create an instance of LimitOrderReason from a JSON string"""
        return LimitOrderReason(json.loads(json_str))


