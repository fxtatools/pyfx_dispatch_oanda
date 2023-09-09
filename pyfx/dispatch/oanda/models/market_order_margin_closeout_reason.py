# coding: utf-8

"""
    OANDA v20 REST API

    The full OANDA v20 REST API Specification. This specification defines how to interact with v20 Accounts, Trades, Orders, Pricing and more.

    The version of the OpenAPI document: 3.0.25
    Contact: api@oanda.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import json
import pprint
import re  # noqa: F401
from aenum import Enum, no_arg





class MarketOrderMarginCloseoutReason(str, Enum):
    """
    The reason that the Market Order was created to perform a margin closeout
    """

    """
    allowed enum values
    """
    MARGIN_CHECK_VIOLATION = 'MARGIN_CHECK_VIOLATION'
    REGULATORY_MARGIN_CALL_VIOLATION = 'REGULATORY_MARGIN_CALL_VIOLATION'
    REGULATORY_MARGIN_CHECK_VIOLATION = 'REGULATORY_MARGIN_CHECK_VIOLATION'

    @classmethod
    def from_json(cls, json_str: str) -> MarketOrderMarginCloseoutReason:
        """Create an instance of MarketOrderMarginCloseoutReason from a JSON string"""
        return MarketOrderMarginCloseoutReason(json.loads(json_str))


