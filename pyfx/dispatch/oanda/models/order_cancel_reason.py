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





class OrderCancelReason(str, Enum):
    """
    The reason that an Order was cancelled.
    """

    """
    allowed enum values
    """
    INTERNAL_SERVER_ERROR = 'INTERNAL_SERVER_ERROR'
    ACCOUNT_LOCKED = 'ACCOUNT_LOCKED'
    ACCOUNT_NEW_POSITIONS_LOCKED = 'ACCOUNT_NEW_POSITIONS_LOCKED'
    ACCOUNT_ORDER_CREATION_LOCKED = 'ACCOUNT_ORDER_CREATION_LOCKED'
    ACCOUNT_ORDER_FILL_LOCKED = 'ACCOUNT_ORDER_FILL_LOCKED'
    CLIENT_REQUEST = 'CLIENT_REQUEST'
    MIGRATION = 'MIGRATION'
    MARKET_HALTED = 'MARKET_HALTED'
    LINKED_TRADE_CLOSED = 'LINKED_TRADE_CLOSED'
    TIME_IN_FORCE_EXPIRED = 'TIME_IN_FORCE_EXPIRED'
    INSUFFICIENT_MARGIN = 'INSUFFICIENT_MARGIN'
    FIFO_VIOLATION = 'FIFO_VIOLATION'
    BOUNDS_VIOLATION = 'BOUNDS_VIOLATION'
    CLIENT_REQUEST_REPLACED = 'CLIENT_REQUEST_REPLACED'
    INSUFFICIENT_LIQUIDITY = 'INSUFFICIENT_LIQUIDITY'
    TAKE_PROFIT_ON_FILL_GTD_TIMESTAMP_IN_PAST = 'TAKE_PROFIT_ON_FILL_GTD_TIMESTAMP_IN_PAST'
    TAKE_PROFIT_ON_FILL_LOSS = 'TAKE_PROFIT_ON_FILL_LOSS'
    LOSING_TAKE_PROFIT = 'LOSING_TAKE_PROFIT'
    STOP_LOSS_ON_FILL_GTD_TIMESTAMP_IN_PAST = 'STOP_LOSS_ON_FILL_GTD_TIMESTAMP_IN_PAST'
    STOP_LOSS_ON_FILL_LOSS = 'STOP_LOSS_ON_FILL_LOSS'
    STOP_LOSS_ON_FILL_PRICE_DISTANCE_MAXIMUM_EXCEEDED = 'STOP_LOSS_ON_FILL_PRICE_DISTANCE_MAXIMUM_EXCEEDED'
    STOP_LOSS_ON_FILL_REQUIRED = 'STOP_LOSS_ON_FILL_REQUIRED'
    STOP_LOSS_ON_FILL_GUARANTEED_REQUIRED = 'STOP_LOSS_ON_FILL_GUARANTEED_REQUIRED'
    STOP_LOSS_ON_FILL_GUARANTEED_NOT_ALLOWED = 'STOP_LOSS_ON_FILL_GUARANTEED_NOT_ALLOWED'
    STOP_LOSS_ON_FILL_GUARANTEED_MINIMUM_DISTANCE_NOT_MET = 'STOP_LOSS_ON_FILL_GUARANTEED_MINIMUM_DISTANCE_NOT_MET'
    STOP_LOSS_ON_FILL_GUARANTEED_LEVEL_RESTRICTION_EXCEEDED = 'STOP_LOSS_ON_FILL_GUARANTEED_LEVEL_RESTRICTION_EXCEEDED'
    STOP_LOSS_ON_FILL_GUARANTEED_HEDGING_NOT_ALLOWED = 'STOP_LOSS_ON_FILL_GUARANTEED_HEDGING_NOT_ALLOWED'
    STOP_LOSS_ON_FILL_TIME_IN_FORCE_INVALID = 'STOP_LOSS_ON_FILL_TIME_IN_FORCE_INVALID'
    STOP_LOSS_ON_FILL_TRIGGER_CONDITION_INVALID = 'STOP_LOSS_ON_FILL_TRIGGER_CONDITION_INVALID'
    TAKE_PROFIT_ON_FILL_PRICE_DISTANCE_MAXIMUM_EXCEEDED = 'TAKE_PROFIT_ON_FILL_PRICE_DISTANCE_MAXIMUM_EXCEEDED'
    TRAILING_STOP_LOSS_ON_FILL_GTD_TIMESTAMP_IN_PAST = 'TRAILING_STOP_LOSS_ON_FILL_GTD_TIMESTAMP_IN_PAST'
    CLIENT_TRADE_ID_ALREADY_EXISTS = 'CLIENT_TRADE_ID_ALREADY_EXISTS'
    POSITION_CLOSEOUT_FAILED = 'POSITION_CLOSEOUT_FAILED'
    OPEN_TRADES_ALLOWED_EXCEEDED = 'OPEN_TRADES_ALLOWED_EXCEEDED'
    PENDING_ORDERS_ALLOWED_EXCEEDED = 'PENDING_ORDERS_ALLOWED_EXCEEDED'
    TAKE_PROFIT_ON_FILL_CLIENT_ORDER_ID_ALREADY_EXISTS = 'TAKE_PROFIT_ON_FILL_CLIENT_ORDER_ID_ALREADY_EXISTS'
    STOP_LOSS_ON_FILL_CLIENT_ORDER_ID_ALREADY_EXISTS = 'STOP_LOSS_ON_FILL_CLIENT_ORDER_ID_ALREADY_EXISTS'
    TRAILING_STOP_LOSS_ON_FILL_CLIENT_ORDER_ID_ALREADY_EXISTS = 'TRAILING_STOP_LOSS_ON_FILL_CLIENT_ORDER_ID_ALREADY_EXISTS'
    POSITION_SIZE_EXCEEDED = 'POSITION_SIZE_EXCEEDED'
    HEDGING_GSLO_VIOLATION = 'HEDGING_GSLO_VIOLATION'
    ACCOUNT_POSITION_VALUE_LIMIT_EXCEEDED = 'ACCOUNT_POSITION_VALUE_LIMIT_EXCEEDED'
    INSTRUMENT_BID_REDUCE_ONLY = 'INSTRUMENT_BID_REDUCE_ONLY'
    INSTRUMENT_ASK_REDUCE_ONLY = 'INSTRUMENT_ASK_REDUCE_ONLY'
    INSTRUMENT_BID_HALTED = 'INSTRUMENT_BID_HALTED'
    INSTRUMENT_ASK_HALTED = 'INSTRUMENT_ASK_HALTED'
    STOP_LOSS_ON_FILL_GUARANTEED_BID_HALTED = 'STOP_LOSS_ON_FILL_GUARANTEED_BID_HALTED'
    STOP_LOSS_ON_FILL_GUARANTEED_ASK_HALTED = 'STOP_LOSS_ON_FILL_GUARANTEED_ASK_HALTED'

    @classmethod
    def from_json(cls, json_str: str) -> OrderCancelReason:
        """Create an instance of OrderCancelReason from a JSON string"""
        return OrderCancelReason(json.loads(json_str))


