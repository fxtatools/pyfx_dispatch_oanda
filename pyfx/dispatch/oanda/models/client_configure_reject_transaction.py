# coding: utf-8

"""
    OANDA v20 REST API

    The full OANDA v20 REST API Specification. This specification defines how to interact with v20 Accounts, Trades, Orders, Pricing and more.

    The version of the OpenAPI document: 3.0.25
    Contact: api@oanda.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, StrictInt, StrictStr, validator

class ClientConfigureRejectTransaction(BaseModel):
    """
    A ClientConfigureRejectTransaction represents the reject of configuration of an Account by a client.
    """
    id: Optional[StrictStr] = Field(None, description="The Transaction's Identifier.")
    time: Optional[StrictStr] = Field(None, description="The date/time when the Transaction was created.")
    user_id: Optional[StrictInt] = Field(None, alias="userID", description="The ID of the user that initiated the creation of the Transaction.")
    account_id: Optional[StrictStr] = Field(None, alias="accountID", description="The ID of the Account the Transaction was created for.")
    batch_id: Optional[StrictStr] = Field(None, alias="batchID", description="The ID of the \"batch\" that the Transaction belongs to. Transactions in the same batch are applied to the Account simultaneously.")
    request_id: Optional[StrictStr] = Field(None, alias="requestID", description="The Request ID of the request which generated the transaction.")
    type: Optional[StrictStr] = Field(None, description="The Type of the Transaction. Always set to \"CLIENT_CONFIGURE_REJECT\" in a ClientConfigureRejectTransaction.")
    alias: Optional[StrictStr] = Field(None, description="The client-provided alias for the Account.")
    margin_rate: Optional[StrictStr] = Field(None, alias="marginRate", description="The margin rate override for the Account.")
    reject_reason: Optional[StrictStr] = Field(None, alias="rejectReason", description="The reason that the Reject Transaction was created")
    additional_properties: Dict[str, Any] = {}
    __properties = ["id", "time", "userID", "accountID", "batchID", "requestID", "type", "alias", "marginRate", "rejectReason"]

    @validator('type')
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('CREATE', 'CLOSE', 'REOPEN', 'CLIENT_CONFIGURE', 'CLIENT_CONFIGURE_REJECT', 'TRANSFER_FUNDS', 'TRANSFER_FUNDS_REJECT', 'MARKET_ORDER', 'MARKET_ORDER_REJECT', 'FIXED_PRICE_ORDER', 'LIMIT_ORDER', 'LIMIT_ORDER_REJECT', 'STOP_ORDER', 'STOP_ORDER_REJECT', 'MARKET_IF_TOUCHED_ORDER', 'MARKET_IF_TOUCHED_ORDER_REJECT', 'TAKE_PROFIT_ORDER', 'TAKE_PROFIT_ORDER_REJECT', 'STOP_LOSS_ORDER', 'STOP_LOSS_ORDER_REJECT', 'TRAILING_STOP_LOSS_ORDER', 'TRAILING_STOP_LOSS_ORDER_REJECT', 'ORDER_FILL', 'ORDER_CANCEL', 'ORDER_CANCEL_REJECT', 'ORDER_CLIENT_EXTENSIONS_MODIFY', 'ORDER_CLIENT_EXTENSIONS_MODIFY_REJECT', 'TRADE_CLIENT_EXTENSIONS_MODIFY', 'TRADE_CLIENT_EXTENSIONS_MODIFY_REJECT', 'MARGIN_CALL_ENTER', 'MARGIN_CALL_EXTEND', 'MARGIN_CALL_EXIT', 'DELAYED_TRADE_CLOSURE', 'DAILY_FINANCING', 'RESET_RESETTABLE_PL'):
            raise ValueError("must be one of enum values ('CREATE', 'CLOSE', 'REOPEN', 'CLIENT_CONFIGURE', 'CLIENT_CONFIGURE_REJECT', 'TRANSFER_FUNDS', 'TRANSFER_FUNDS_REJECT', 'MARKET_ORDER', 'MARKET_ORDER_REJECT', 'FIXED_PRICE_ORDER', 'LIMIT_ORDER', 'LIMIT_ORDER_REJECT', 'STOP_ORDER', 'STOP_ORDER_REJECT', 'MARKET_IF_TOUCHED_ORDER', 'MARKET_IF_TOUCHED_ORDER_REJECT', 'TAKE_PROFIT_ORDER', 'TAKE_PROFIT_ORDER_REJECT', 'STOP_LOSS_ORDER', 'STOP_LOSS_ORDER_REJECT', 'TRAILING_STOP_LOSS_ORDER', 'TRAILING_STOP_LOSS_ORDER_REJECT', 'ORDER_FILL', 'ORDER_CANCEL', 'ORDER_CANCEL_REJECT', 'ORDER_CLIENT_EXTENSIONS_MODIFY', 'ORDER_CLIENT_EXTENSIONS_MODIFY_REJECT', 'TRADE_CLIENT_EXTENSIONS_MODIFY', 'TRADE_CLIENT_EXTENSIONS_MODIFY_REJECT', 'MARGIN_CALL_ENTER', 'MARGIN_CALL_EXTEND', 'MARGIN_CALL_EXIT', 'DELAYED_TRADE_CLOSURE', 'DAILY_FINANCING', 'RESET_RESETTABLE_PL')")
        return value

    @validator('reject_reason')
    def reject_reason_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('INTERNAL_SERVER_ERROR', 'INSTRUMENT_PRICE_UNKNOWN', 'ACCOUNT_NOT_ACTIVE', 'ACCOUNT_LOCKED', 'ACCOUNT_ORDER_CREATION_LOCKED', 'ACCOUNT_CONFIGURATION_LOCKED', 'ACCOUNT_DEPOSIT_LOCKED', 'ACCOUNT_WITHDRAWAL_LOCKED', 'ACCOUNT_ORDER_CANCEL_LOCKED', 'INSTRUMENT_NOT_TRADEABLE', 'PENDING_ORDERS_ALLOWED_EXCEEDED', 'ORDER_ID_UNSPECIFIED', 'ORDER_DOESNT_EXIST', 'ORDER_IDENTIFIER_INCONSISTENCY', 'TRADE_ID_UNSPECIFIED', 'TRADE_DOESNT_EXIST', 'TRADE_IDENTIFIER_INCONSISTENCY', 'INSUFFICIENT_MARGIN', 'INSTRUMENT_MISSING', 'INSTRUMENT_UNKNOWN', 'UNITS_MISSING', 'UNITS_INVALID', 'UNITS_PRECISION_EXCEEDED', 'UNITS_LIMIT_EXCEEDED', 'UNITS_MIMIMUM_NOT_MET', 'PRICE_MISSING', 'PRICE_INVALID', 'PRICE_PRECISION_EXCEEDED', 'PRICE_DISTANCE_MISSING', 'PRICE_DISTANCE_INVALID', 'PRICE_DISTANCE_PRECISION_EXCEEDED', 'PRICE_DISTANCE_MAXIMUM_EXCEEDED', 'PRICE_DISTANCE_MINIMUM_NOT_MET', 'TIME_IN_FORCE_MISSING', 'TIME_IN_FORCE_INVALID', 'TIME_IN_FORCE_GTD_TIMESTAMP_MISSING', 'TIME_IN_FORCE_GTD_TIMESTAMP_IN_PAST', 'PRICE_BOUND_INVALID', 'PRICE_BOUND_PRECISION_EXCEEDED', 'ORDERS_ON_FILL_DUPLICATE_CLIENT_ORDER_IDS', 'TRADE_ON_FILL_CLIENT_EXTENSIONS_NOT_SUPPORTED', 'CLIENT_ORDER_ID_INVALID', 'CLIENT_ORDER_ID_ALREADY_EXISTS', 'CLIENT_ORDER_TAG_INVALID', 'CLIENT_ORDER_COMMENT_INVALID', 'CLIENT_TRADE_ID_INVALID', 'CLIENT_TRADE_ID_ALREADY_EXISTS', 'CLIENT_TRADE_TAG_INVALID', 'CLIENT_TRADE_COMMENT_INVALID', 'ORDER_FILL_POSITION_ACTION_MISSING', 'ORDER_FILL_POSITION_ACTION_INVALID', 'TRIGGER_CONDITION_MISSING', 'TRIGGER_CONDITION_INVALID', 'ORDER_PARTIAL_FILL_OPTION_MISSING', 'ORDER_PARTIAL_FILL_OPTION_INVALID', 'INVALID_REISSUE_IMMEDIATE_PARTIAL_FILL', 'TAKE_PROFIT_ORDER_ALREADY_EXISTS', 'TAKE_PROFIT_ON_FILL_PRICE_MISSING', 'TAKE_PROFIT_ON_FILL_PRICE_INVALID', 'TAKE_PROFIT_ON_FILL_PRICE_PRECISION_EXCEEDED', 'TAKE_PROFIT_ON_FILL_TIME_IN_FORCE_MISSING', 'TAKE_PROFIT_ON_FILL_TIME_IN_FORCE_INVALID', 'TAKE_PROFIT_ON_FILL_GTD_TIMESTAMP_MISSING', 'TAKE_PROFIT_ON_FILL_GTD_TIMESTAMP_IN_PAST', 'TAKE_PROFIT_ON_FILL_CLIENT_ORDER_ID_INVALID', 'TAKE_PROFIT_ON_FILL_CLIENT_ORDER_TAG_INVALID', 'TAKE_PROFIT_ON_FILL_CLIENT_ORDER_COMMENT_INVALID', 'TAKE_PROFIT_ON_FILL_TRIGGER_CONDITION_MISSING', 'TAKE_PROFIT_ON_FILL_TRIGGER_CONDITION_INVALID', 'STOP_LOSS_ORDER_ALREADY_EXISTS', 'STOP_LOSS_ORDER_GUARANTEED_REQUIRED', 'STOP_LOSS_ORDER_GUARANTEED_PRICE_WITHIN_SPREAD', 'STOP_LOSS_ORDER_GUARANTEED_NOT_ALLOWED', 'STOP_LOSS_ORDER_GUARANTEED_HALTED_CREATE_VIOLATION', 'STOP_LOSS_ORDER_GUARANTEED_HALTED_TIGHTEN_VIOLATION', 'STOP_LOSS_ORDER_GUARANTEED_HEDGING_NOT_ALLOWED', 'STOP_LOSS_ORDER_GUARANTEED_MINIMUM_DISTANCE_NOT_MET', 'STOP_LOSS_ORDER_NOT_CANCELABLE', 'STOP_LOSS_ORDER_NOT_REPLACEABLE', 'STOP_LOSS_ORDER_GUARANTEED_LEVEL_RESTRICTION_EXCEEDED', 'STOP_LOSS_ORDER_PRICE_AND_DISTANCE_BOTH_SPECIFIED', 'STOP_LOSS_ORDER_PRICE_AND_DISTANCE_BOTH_MISSING', 'STOP_LOSS_ON_FILL_REQUIRED_FOR_PENDING_ORDER', 'STOP_LOSS_ON_FILL_GUARANTEED_NOT_ALLOWED', 'STOP_LOSS_ON_FILL_GUARANTEED_REQUIRED', 'STOP_LOSS_ON_FILL_PRICE_MISSING', 'STOP_LOSS_ON_FILL_PRICE_INVALID', 'STOP_LOSS_ON_FILL_PRICE_PRECISION_EXCEEDED', 'STOP_LOSS_ON_FILL_GUARANTEED_MINIMUM_DISTANCE_NOT_MET', 'STOP_LOSS_ON_FILL_GUARANTEED_LEVEL_RESTRICTION_EXCEEDED', 'STOP_LOSS_ON_FILL_DISTANCE_INVALID', 'STOP_LOSS_ON_FILL_PRICE_DISTANCE_MAXIMUM_EXCEEDED', 'STOP_LOSS_ON_FILL_DISTANCE_PRECISION_EXCEEDED', 'STOP_LOSS_ON_FILL_PRICE_AND_DISTANCE_BOTH_SPECIFIED', 'STOP_LOSS_ON_FILL_PRICE_AND_DISTANCE_BOTH_MISSING', 'STOP_LOSS_ON_FILL_TIME_IN_FORCE_MISSING', 'STOP_LOSS_ON_FILL_TIME_IN_FORCE_INVALID', 'STOP_LOSS_ON_FILL_GTD_TIMESTAMP_MISSING', 'STOP_LOSS_ON_FILL_GTD_TIMESTAMP_IN_PAST', 'STOP_LOSS_ON_FILL_CLIENT_ORDER_ID_INVALID', 'STOP_LOSS_ON_FILL_CLIENT_ORDER_TAG_INVALID', 'STOP_LOSS_ON_FILL_CLIENT_ORDER_COMMENT_INVALID', 'STOP_LOSS_ON_FILL_TRIGGER_CONDITION_MISSING', 'STOP_LOSS_ON_FILL_TRIGGER_CONDITION_INVALID', 'TRAILING_STOP_LOSS_ORDER_ALREADY_EXISTS', 'TRAILING_STOP_LOSS_ON_FILL_PRICE_DISTANCE_MISSING', 'TRAILING_STOP_LOSS_ON_FILL_PRICE_DISTANCE_INVALID', 'TRAILING_STOP_LOSS_ON_FILL_PRICE_DISTANCE_PRECISION_EXCEEDED', 'TRAILING_STOP_LOSS_ON_FILL_PRICE_DISTANCE_MAXIMUM_EXCEEDED', 'TRAILING_STOP_LOSS_ON_FILL_PRICE_DISTANCE_MINIMUM_NOT_MET', 'TRAILING_STOP_LOSS_ON_FILL_TIME_IN_FORCE_MISSING', 'TRAILING_STOP_LOSS_ON_FILL_TIME_IN_FORCE_INVALID', 'TRAILING_STOP_LOSS_ON_FILL_GTD_TIMESTAMP_MISSING', 'TRAILING_STOP_LOSS_ON_FILL_GTD_TIMESTAMP_IN_PAST', 'TRAILING_STOP_LOSS_ON_FILL_CLIENT_ORDER_ID_INVALID', 'TRAILING_STOP_LOSS_ON_FILL_CLIENT_ORDER_TAG_INVALID', 'TRAILING_STOP_LOSS_ON_FILL_CLIENT_ORDER_COMMENT_INVALID', 'TRAILING_STOP_LOSS_ORDERS_NOT_SUPPORTED', 'TRAILING_STOP_LOSS_ON_FILL_TRIGGER_CONDITION_MISSING', 'TRAILING_STOP_LOSS_ON_FILL_TRIGGER_CONDITION_INVALID', 'CLOSE_TRADE_TYPE_MISSING', 'CLOSE_TRADE_PARTIAL_UNITS_MISSING', 'CLOSE_TRADE_UNITS_EXCEED_TRADE_SIZE', 'CLOSEOUT_POSITION_DOESNT_EXIST', 'CLOSEOUT_POSITION_INCOMPLETE_SPECIFICATION', 'CLOSEOUT_POSITION_UNITS_EXCEED_POSITION_SIZE', 'CLOSEOUT_POSITION_REJECT', 'CLOSEOUT_POSITION_PARTIAL_UNITS_MISSING', 'MARKUP_GROUP_ID_INVALID', 'POSITION_AGGREGATION_MODE_INVALID', 'ADMIN_CONFIGURE_DATA_MISSING', 'MARGIN_RATE_INVALID', 'MARGIN_RATE_WOULD_TRIGGER_CLOSEOUT', 'ALIAS_INVALID', 'CLIENT_CONFIGURE_DATA_MISSING', 'MARGIN_RATE_WOULD_TRIGGER_MARGIN_CALL', 'AMOUNT_INVALID', 'INSUFFICIENT_FUNDS', 'AMOUNT_MISSING', 'FUNDING_REASON_MISSING', 'CLIENT_EXTENSIONS_DATA_MISSING', 'REPLACING_ORDER_INVALID', 'REPLACING_TRADE_ID_INVALID'):
            raise ValueError("must be one of enum values ('INTERNAL_SERVER_ERROR', 'INSTRUMENT_PRICE_UNKNOWN', 'ACCOUNT_NOT_ACTIVE', 'ACCOUNT_LOCKED', 'ACCOUNT_ORDER_CREATION_LOCKED', 'ACCOUNT_CONFIGURATION_LOCKED', 'ACCOUNT_DEPOSIT_LOCKED', 'ACCOUNT_WITHDRAWAL_LOCKED', 'ACCOUNT_ORDER_CANCEL_LOCKED', 'INSTRUMENT_NOT_TRADEABLE', 'PENDING_ORDERS_ALLOWED_EXCEEDED', 'ORDER_ID_UNSPECIFIED', 'ORDER_DOESNT_EXIST', 'ORDER_IDENTIFIER_INCONSISTENCY', 'TRADE_ID_UNSPECIFIED', 'TRADE_DOESNT_EXIST', 'TRADE_IDENTIFIER_INCONSISTENCY', 'INSUFFICIENT_MARGIN', 'INSTRUMENT_MISSING', 'INSTRUMENT_UNKNOWN', 'UNITS_MISSING', 'UNITS_INVALID', 'UNITS_PRECISION_EXCEEDED', 'UNITS_LIMIT_EXCEEDED', 'UNITS_MIMIMUM_NOT_MET', 'PRICE_MISSING', 'PRICE_INVALID', 'PRICE_PRECISION_EXCEEDED', 'PRICE_DISTANCE_MISSING', 'PRICE_DISTANCE_INVALID', 'PRICE_DISTANCE_PRECISION_EXCEEDED', 'PRICE_DISTANCE_MAXIMUM_EXCEEDED', 'PRICE_DISTANCE_MINIMUM_NOT_MET', 'TIME_IN_FORCE_MISSING', 'TIME_IN_FORCE_INVALID', 'TIME_IN_FORCE_GTD_TIMESTAMP_MISSING', 'TIME_IN_FORCE_GTD_TIMESTAMP_IN_PAST', 'PRICE_BOUND_INVALID', 'PRICE_BOUND_PRECISION_EXCEEDED', 'ORDERS_ON_FILL_DUPLICATE_CLIENT_ORDER_IDS', 'TRADE_ON_FILL_CLIENT_EXTENSIONS_NOT_SUPPORTED', 'CLIENT_ORDER_ID_INVALID', 'CLIENT_ORDER_ID_ALREADY_EXISTS', 'CLIENT_ORDER_TAG_INVALID', 'CLIENT_ORDER_COMMENT_INVALID', 'CLIENT_TRADE_ID_INVALID', 'CLIENT_TRADE_ID_ALREADY_EXISTS', 'CLIENT_TRADE_TAG_INVALID', 'CLIENT_TRADE_COMMENT_INVALID', 'ORDER_FILL_POSITION_ACTION_MISSING', 'ORDER_FILL_POSITION_ACTION_INVALID', 'TRIGGER_CONDITION_MISSING', 'TRIGGER_CONDITION_INVALID', 'ORDER_PARTIAL_FILL_OPTION_MISSING', 'ORDER_PARTIAL_FILL_OPTION_INVALID', 'INVALID_REISSUE_IMMEDIATE_PARTIAL_FILL', 'TAKE_PROFIT_ORDER_ALREADY_EXISTS', 'TAKE_PROFIT_ON_FILL_PRICE_MISSING', 'TAKE_PROFIT_ON_FILL_PRICE_INVALID', 'TAKE_PROFIT_ON_FILL_PRICE_PRECISION_EXCEEDED', 'TAKE_PROFIT_ON_FILL_TIME_IN_FORCE_MISSING', 'TAKE_PROFIT_ON_FILL_TIME_IN_FORCE_INVALID', 'TAKE_PROFIT_ON_FILL_GTD_TIMESTAMP_MISSING', 'TAKE_PROFIT_ON_FILL_GTD_TIMESTAMP_IN_PAST', 'TAKE_PROFIT_ON_FILL_CLIENT_ORDER_ID_INVALID', 'TAKE_PROFIT_ON_FILL_CLIENT_ORDER_TAG_INVALID', 'TAKE_PROFIT_ON_FILL_CLIENT_ORDER_COMMENT_INVALID', 'TAKE_PROFIT_ON_FILL_TRIGGER_CONDITION_MISSING', 'TAKE_PROFIT_ON_FILL_TRIGGER_CONDITION_INVALID', 'STOP_LOSS_ORDER_ALREADY_EXISTS', 'STOP_LOSS_ORDER_GUARANTEED_REQUIRED', 'STOP_LOSS_ORDER_GUARANTEED_PRICE_WITHIN_SPREAD', 'STOP_LOSS_ORDER_GUARANTEED_NOT_ALLOWED', 'STOP_LOSS_ORDER_GUARANTEED_HALTED_CREATE_VIOLATION', 'STOP_LOSS_ORDER_GUARANTEED_HALTED_TIGHTEN_VIOLATION', 'STOP_LOSS_ORDER_GUARANTEED_HEDGING_NOT_ALLOWED', 'STOP_LOSS_ORDER_GUARANTEED_MINIMUM_DISTANCE_NOT_MET', 'STOP_LOSS_ORDER_NOT_CANCELABLE', 'STOP_LOSS_ORDER_NOT_REPLACEABLE', 'STOP_LOSS_ORDER_GUARANTEED_LEVEL_RESTRICTION_EXCEEDED', 'STOP_LOSS_ORDER_PRICE_AND_DISTANCE_BOTH_SPECIFIED', 'STOP_LOSS_ORDER_PRICE_AND_DISTANCE_BOTH_MISSING', 'STOP_LOSS_ON_FILL_REQUIRED_FOR_PENDING_ORDER', 'STOP_LOSS_ON_FILL_GUARANTEED_NOT_ALLOWED', 'STOP_LOSS_ON_FILL_GUARANTEED_REQUIRED', 'STOP_LOSS_ON_FILL_PRICE_MISSING', 'STOP_LOSS_ON_FILL_PRICE_INVALID', 'STOP_LOSS_ON_FILL_PRICE_PRECISION_EXCEEDED', 'STOP_LOSS_ON_FILL_GUARANTEED_MINIMUM_DISTANCE_NOT_MET', 'STOP_LOSS_ON_FILL_GUARANTEED_LEVEL_RESTRICTION_EXCEEDED', 'STOP_LOSS_ON_FILL_DISTANCE_INVALID', 'STOP_LOSS_ON_FILL_PRICE_DISTANCE_MAXIMUM_EXCEEDED', 'STOP_LOSS_ON_FILL_DISTANCE_PRECISION_EXCEEDED', 'STOP_LOSS_ON_FILL_PRICE_AND_DISTANCE_BOTH_SPECIFIED', 'STOP_LOSS_ON_FILL_PRICE_AND_DISTANCE_BOTH_MISSING', 'STOP_LOSS_ON_FILL_TIME_IN_FORCE_MISSING', 'STOP_LOSS_ON_FILL_TIME_IN_FORCE_INVALID', 'STOP_LOSS_ON_FILL_GTD_TIMESTAMP_MISSING', 'STOP_LOSS_ON_FILL_GTD_TIMESTAMP_IN_PAST', 'STOP_LOSS_ON_FILL_CLIENT_ORDER_ID_INVALID', 'STOP_LOSS_ON_FILL_CLIENT_ORDER_TAG_INVALID', 'STOP_LOSS_ON_FILL_CLIENT_ORDER_COMMENT_INVALID', 'STOP_LOSS_ON_FILL_TRIGGER_CONDITION_MISSING', 'STOP_LOSS_ON_FILL_TRIGGER_CONDITION_INVALID', 'TRAILING_STOP_LOSS_ORDER_ALREADY_EXISTS', 'TRAILING_STOP_LOSS_ON_FILL_PRICE_DISTANCE_MISSING', 'TRAILING_STOP_LOSS_ON_FILL_PRICE_DISTANCE_INVALID', 'TRAILING_STOP_LOSS_ON_FILL_PRICE_DISTANCE_PRECISION_EXCEEDED', 'TRAILING_STOP_LOSS_ON_FILL_PRICE_DISTANCE_MAXIMUM_EXCEEDED', 'TRAILING_STOP_LOSS_ON_FILL_PRICE_DISTANCE_MINIMUM_NOT_MET', 'TRAILING_STOP_LOSS_ON_FILL_TIME_IN_FORCE_MISSING', 'TRAILING_STOP_LOSS_ON_FILL_TIME_IN_FORCE_INVALID', 'TRAILING_STOP_LOSS_ON_FILL_GTD_TIMESTAMP_MISSING', 'TRAILING_STOP_LOSS_ON_FILL_GTD_TIMESTAMP_IN_PAST', 'TRAILING_STOP_LOSS_ON_FILL_CLIENT_ORDER_ID_INVALID', 'TRAILING_STOP_LOSS_ON_FILL_CLIENT_ORDER_TAG_INVALID', 'TRAILING_STOP_LOSS_ON_FILL_CLIENT_ORDER_COMMENT_INVALID', 'TRAILING_STOP_LOSS_ORDERS_NOT_SUPPORTED', 'TRAILING_STOP_LOSS_ON_FILL_TRIGGER_CONDITION_MISSING', 'TRAILING_STOP_LOSS_ON_FILL_TRIGGER_CONDITION_INVALID', 'CLOSE_TRADE_TYPE_MISSING', 'CLOSE_TRADE_PARTIAL_UNITS_MISSING', 'CLOSE_TRADE_UNITS_EXCEED_TRADE_SIZE', 'CLOSEOUT_POSITION_DOESNT_EXIST', 'CLOSEOUT_POSITION_INCOMPLETE_SPECIFICATION', 'CLOSEOUT_POSITION_UNITS_EXCEED_POSITION_SIZE', 'CLOSEOUT_POSITION_REJECT', 'CLOSEOUT_POSITION_PARTIAL_UNITS_MISSING', 'MARKUP_GROUP_ID_INVALID', 'POSITION_AGGREGATION_MODE_INVALID', 'ADMIN_CONFIGURE_DATA_MISSING', 'MARGIN_RATE_INVALID', 'MARGIN_RATE_WOULD_TRIGGER_CLOSEOUT', 'ALIAS_INVALID', 'CLIENT_CONFIGURE_DATA_MISSING', 'MARGIN_RATE_WOULD_TRIGGER_MARGIN_CALL', 'AMOUNT_INVALID', 'INSUFFICIENT_FUNDS', 'AMOUNT_MISSING', 'FUNDING_REASON_MISSING', 'CLIENT_EXTENSIONS_DATA_MISSING', 'REPLACING_ORDER_INVALID', 'REPLACING_TRADE_ID_INVALID')")
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
    def from_json(cls, json_str: str) -> ClientConfigureRejectTransaction:
        """Create an instance of ClientConfigureRejectTransaction from a JSON string"""
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
    def from_dict(cls, obj: dict) -> ClientConfigureRejectTransaction:
        """Create an instance of ClientConfigureRejectTransaction from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ClientConfigureRejectTransaction.parse_obj(obj)

        _obj = ClientConfigureRejectTransaction.parse_obj({
            "id": obj.get("id"),
            "time": obj.get("time"),
            "user_id": obj.get("userID"),
            "account_id": obj.get("accountID"),
            "batch_id": obj.get("batchID"),
            "request_id": obj.get("requestID"),
            "type": obj.get("type"),
            "alias": obj.get("alias"),
            "margin_rate": obj.get("marginRate"),
            "reject_reason": obj.get("rejectReason")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj


