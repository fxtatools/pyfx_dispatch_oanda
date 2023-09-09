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





class PositionAggregationMode(str, Enum):
    """
    The way that position values for an Account are calculated and aggregated.
    """

    """
    allowed enum values
    """
    ABSOLUTE_SUM = 'ABSOLUTE_SUM'
    MAXIMAL_SIDE = 'MAXIMAL_SIDE'
    NET_SUM = 'NET_SUM'

    @classmethod
    def from_json(cls, json_str: str) -> PositionAggregationMode:
        """Create an instance of PositionAggregationMode from a JSON string"""
        return PositionAggregationMode(json.loads(json_str))


