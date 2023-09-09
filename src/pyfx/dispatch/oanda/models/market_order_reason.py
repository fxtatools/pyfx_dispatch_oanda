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





class MarketOrderReason(str, Enum):
    """
    The reason that the Market Order was created
    """

    """
    allowed enum values
    """
    CLIENT_ORDER = 'CLIENT_ORDER'
    TRADE_CLOSE = 'TRADE_CLOSE'
    POSITION_CLOSEOUT = 'POSITION_CLOSEOUT'
    MARGIN_CLOSEOUT = 'MARGIN_CLOSEOUT'
    DELAYED_TRADE_CLOSE = 'DELAYED_TRADE_CLOSE'

    @classmethod
    def from_json(cls, json_str: str) -> MarketOrderReason:
        """Create an instance of MarketOrderReason from a JSON string"""
        return MarketOrderReason(json.loads(json_str))

