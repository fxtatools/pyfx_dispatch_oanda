# coding: utf-8

"""
    OANDA v20 REST API

    The full OANDA v20 REST API Specification. This specification defines how to interact with v20 Accounts, Trades, Orders, Pricing and more.

    The version of the OpenAPI document: 3.0.25

    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, StrictInt, StrictStr, validator

class OrderCancelTransaction(BaseModel):
    """
    An OrderCancelTransaction represents the cancellation of an Order in the client's Account.
    """
    id: Optional[StrictStr] = Field(None, description="The Transaction's Identifier.")
    time: Optional[StrictStr] = Field(None, description="The date/time when the Transaction was created.")
    user_id: Optional[StrictInt] = Field(None, alias="userID", description="The ID of the user that initiated the creation of the Transaction.")
    account_id: Optional[StrictStr] = Field(None, alias="accountID", description="The ID of the Account the Transaction was created for.")
    batch_id: Optional[StrictStr] = Field(None, alias="batchID", description="The ID of the \"batch\" that the Transaction belongs to. Transactions in the same batch are applied to the Account simultaneously.")
    request_id: Optional[StrictStr] = Field(None, alias="requestID", description="The Request ID of the request which generated the transaction.")
    type: Optional[StrictStr] = Field(None, description="The Type of the Transaction. Always set to \"ORDER_CANCEL\" for an OrderCancelTransaction.")
    order_id: Optional[StrictStr] = Field(None, alias="orderID", description="The ID of the Order cancelled")
    client_order_id: Optional[StrictStr] = Field(None, alias="clientOrderID", description="The client ID of the Order cancelled (only provided if the Order has a client Order ID).")
    reason: Optional[StrictStr] = Field(None, description="The reason that the Order was cancelled.")
    replaced_by_order_id: Optional[StrictStr] = Field(None, alias="replacedByOrderID", description="The ID of the Order that replaced this Order (only provided if this Order was cancelled for replacement).")
    additional_properties: Dict[str, Any] = {}
    __properties = ["id", "time", "userID", "accountID", "batchID", "requestID", "type", "orderID", "clientOrderID", "reason", "replacedByOrderID"]

    @validator('type')
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('CREATE', 'CLOSE', 'REOPEN', 'CLIENT_CONFIGURE', 'CLIENT_CONFIGURE_REJECT', 'TRANSFER_FUNDS', 'TRANSFER_FUNDS_REJECT', 'MARKET_ORDER', 'MARKET_ORDER_REJECT', 'FIXED_PRICE_ORDER', 'LIMIT_ORDER', 'LIMIT_ORDER_REJECT', 'STOP_ORDER', 'STOP_ORDER_REJECT', 'MARKET_IF_TOUCHED_ORDER', 'MARKET_IF_TOUCHED_ORDER_REJECT', 'TAKE_PROFIT_ORDER', 'TAKE_PROFIT_ORDER_REJECT', 'STOP_LOSS_ORDER', 'STOP_LOSS_ORDER_REJECT', 'TRAILING_STOP_LOSS_ORDER', 'TRAILING_STOP_LOSS_ORDER_REJECT', 'ORDER_FILL', 'ORDER_CANCEL', 'ORDER_CANCEL_REJECT', 'ORDER_CLIENT_EXTENSIONS_MODIFY', 'ORDER_CLIENT_EXTENSIONS_MODIFY_REJECT', 'TRADE_CLIENT_EXTENSIONS_MODIFY', 'TRADE_CLIENT_EXTENSIONS_MODIFY_REJECT', 'MARGIN_CALL_ENTER', 'MARGIN_CALL_EXTEND', 'MARGIN_CALL_EXIT', 'DELAYED_TRADE_CLOSURE', 'DAILY_FINANCING', 'RESET_RESETTABLE_PL'):
            raise ValueError("must be one of enum values ('CREATE', 'CLOSE', 'REOPEN', 'CLIENT_CONFIGURE', 'CLIENT_CONFIGURE_REJECT', 'TRANSFER_FUNDS', 'TRANSFER_FUNDS_REJECT', 'MARKET_ORDER', 'MARKET_ORDER_REJECT', 'FIXED_PRICE_ORDER', 'LIMIT_ORDER', 'LIMIT_ORDER_REJECT', 'STOP_ORDER', 'STOP_ORDER_REJECT', 'MARKET_IF_TOUCHED_ORDER', 'MARKET_IF_TOUCHED_ORDER_REJECT', 'TAKE_PROFIT_ORDER', 'TAKE_PROFIT_ORDER_REJECT', 'STOP_LOSS_ORDER', 'STOP_LOSS_ORDER_REJECT', 'TRAILING_STOP_LOSS_ORDER', 'TRAILING_STOP_LOSS_ORDER_REJECT', 'ORDER_FILL', 'ORDER_CANCEL', 'ORDER_CANCEL_REJECT', 'ORDER_CLIENT_EXTENSIONS_MODIFY', 'ORDER_CLIENT_EXTENSIONS_MODIFY_REJECT', 'TRADE_CLIENT_EXTENSIONS_MODIFY', 'TRADE_CLIENT_EXTENSIONS_MODIFY_REJECT', 'MARGIN_CALL_ENTER', 'MARGIN_CALL_EXTEND', 'MARGIN_CALL_EXIT', 'DELAYED_TRADE_CLOSURE', 'DAILY_FINANCING', 'RESET_RESETTABLE_PL')")
        return value

    @validator('reason')
    def reason_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('INTERNAL_SERVER_ERROR', 'ACCOUNT_LOCKED', 'ACCOUNT_NEW_POSITIONS_LOCKED', 'ACCOUNT_ORDER_CREATION_LOCKED', 'ACCOUNT_ORDER_FILL_LOCKED', 'CLIENT_REQUEST', 'MIGRATION', 'MARKET_HALTED', 'LINKED_TRADE_CLOSED', 'TIME_IN_FORCE_EXPIRED', 'INSUFFICIENT_MARGIN', 'FIFO_VIOLATION', 'BOUNDS_VIOLATION', 'CLIENT_REQUEST_REPLACED', 'INSUFFICIENT_LIQUIDITY', 'TAKE_PROFIT_ON_FILL_GTD_TIMESTAMP_IN_PAST', 'TAKE_PROFIT_ON_FILL_LOSS', 'LOSING_TAKE_PROFIT', 'STOP_LOSS_ON_FILL_GTD_TIMESTAMP_IN_PAST', 'STOP_LOSS_ON_FILL_LOSS', 'STOP_LOSS_ON_FILL_PRICE_DISTANCE_MAXIMUM_EXCEEDED', 'STOP_LOSS_ON_FILL_REQUIRED', 'STOP_LOSS_ON_FILL_GUARANTEED_REQUIRED', 'STOP_LOSS_ON_FILL_GUARANTEED_NOT_ALLOWED', 'STOP_LOSS_ON_FILL_GUARANTEED_MINIMUM_DISTANCE_NOT_MET', 'STOP_LOSS_ON_FILL_GUARANTEED_LEVEL_RESTRICTION_EXCEEDED', 'STOP_LOSS_ON_FILL_GUARANTEED_HEDGING_NOT_ALLOWED', 'STOP_LOSS_ON_FILL_TIME_IN_FORCE_INVALID', 'STOP_LOSS_ON_FILL_TRIGGER_CONDITION_INVALID', 'TAKE_PROFIT_ON_FILL_PRICE_DISTANCE_MAXIMUM_EXCEEDED', 'TRAILING_STOP_LOSS_ON_FILL_GTD_TIMESTAMP_IN_PAST', 'CLIENT_TRADE_ID_ALREADY_EXISTS', 'POSITION_CLOSEOUT_FAILED', 'OPEN_TRADES_ALLOWED_EXCEEDED', 'PENDING_ORDERS_ALLOWED_EXCEEDED', 'TAKE_PROFIT_ON_FILL_CLIENT_ORDER_ID_ALREADY_EXISTS', 'STOP_LOSS_ON_FILL_CLIENT_ORDER_ID_ALREADY_EXISTS', 'TRAILING_STOP_LOSS_ON_FILL_CLIENT_ORDER_ID_ALREADY_EXISTS', 'POSITION_SIZE_EXCEEDED', 'HEDGING_GSLO_VIOLATION', 'ACCOUNT_POSITION_VALUE_LIMIT_EXCEEDED', 'INSTRUMENT_BID_REDUCE_ONLY', 'INSTRUMENT_ASK_REDUCE_ONLY', 'INSTRUMENT_BID_HALTED', 'INSTRUMENT_ASK_HALTED', 'STOP_LOSS_ON_FILL_GUARANTEED_BID_HALTED', 'STOP_LOSS_ON_FILL_GUARANTEED_ASK_HALTED'):
            raise ValueError("must be one of enum values ('INTERNAL_SERVER_ERROR', 'ACCOUNT_LOCKED', 'ACCOUNT_NEW_POSITIONS_LOCKED', 'ACCOUNT_ORDER_CREATION_LOCKED', 'ACCOUNT_ORDER_FILL_LOCKED', 'CLIENT_REQUEST', 'MIGRATION', 'MARKET_HALTED', 'LINKED_TRADE_CLOSED', 'TIME_IN_FORCE_EXPIRED', 'INSUFFICIENT_MARGIN', 'FIFO_VIOLATION', 'BOUNDS_VIOLATION', 'CLIENT_REQUEST_REPLACED', 'INSUFFICIENT_LIQUIDITY', 'TAKE_PROFIT_ON_FILL_GTD_TIMESTAMP_IN_PAST', 'TAKE_PROFIT_ON_FILL_LOSS', 'LOSING_TAKE_PROFIT', 'STOP_LOSS_ON_FILL_GTD_TIMESTAMP_IN_PAST', 'STOP_LOSS_ON_FILL_LOSS', 'STOP_LOSS_ON_FILL_PRICE_DISTANCE_MAXIMUM_EXCEEDED', 'STOP_LOSS_ON_FILL_REQUIRED', 'STOP_LOSS_ON_FILL_GUARANTEED_REQUIRED', 'STOP_LOSS_ON_FILL_GUARANTEED_NOT_ALLOWED', 'STOP_LOSS_ON_FILL_GUARANTEED_MINIMUM_DISTANCE_NOT_MET', 'STOP_LOSS_ON_FILL_GUARANTEED_LEVEL_RESTRICTION_EXCEEDED', 'STOP_LOSS_ON_FILL_GUARANTEED_HEDGING_NOT_ALLOWED', 'STOP_LOSS_ON_FILL_TIME_IN_FORCE_INVALID', 'STOP_LOSS_ON_FILL_TRIGGER_CONDITION_INVALID', 'TAKE_PROFIT_ON_FILL_PRICE_DISTANCE_MAXIMUM_EXCEEDED', 'TRAILING_STOP_LOSS_ON_FILL_GTD_TIMESTAMP_IN_PAST', 'CLIENT_TRADE_ID_ALREADY_EXISTS', 'POSITION_CLOSEOUT_FAILED', 'OPEN_TRADES_ALLOWED_EXCEEDED', 'PENDING_ORDERS_ALLOWED_EXCEEDED', 'TAKE_PROFIT_ON_FILL_CLIENT_ORDER_ID_ALREADY_EXISTS', 'STOP_LOSS_ON_FILL_CLIENT_ORDER_ID_ALREADY_EXISTS', 'TRAILING_STOP_LOSS_ON_FILL_CLIENT_ORDER_ID_ALREADY_EXISTS', 'POSITION_SIZE_EXCEEDED', 'HEDGING_GSLO_VIOLATION', 'ACCOUNT_POSITION_VALUE_LIMIT_EXCEEDED', 'INSTRUMENT_BID_REDUCE_ONLY', 'INSTRUMENT_ASK_REDUCE_ONLY', 'INSTRUMENT_BID_HALTED', 'INSTRUMENT_ASK_HALTED', 'STOP_LOSS_ON_FILL_GUARANTEED_BID_HALTED', 'STOP_LOSS_ON_FILL_GUARANTEED_ASK_HALTED')")
        return value

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> OrderCancelTransaction:
        """Create an instance of OrderCancelTransaction from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "additional_properties"
                          },
                          exclude_none=True)
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> OrderCancelTransaction:
        """Create an instance of OrderCancelTransaction from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return OrderCancelTransaction.parse_obj(obj)

        _obj = OrderCancelTransaction.parse_obj({
            "id": obj.get("id"),
            "time": obj.get("time"),
            "user_id": obj.get("userID"),
            "account_id": obj.get("accountID"),
            "batch_id": obj.get("batchID"),
            "request_id": obj.get("requestID"),
            "type": obj.get("type"),
            "order_id": obj.get("orderID"),
            "client_order_id": obj.get("clientOrderID"),
            "reason": obj.get("reason"),
            "replaced_by_order_id": obj.get("replacedByOrderID")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj


