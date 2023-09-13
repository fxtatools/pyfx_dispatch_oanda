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
from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr, validator
from pyfx.dispatch.oanda.models.client_extensions import ClientExtensions

class StopLossOrderRejectTransaction(BaseModel):
    """
    A StopLossOrderRejectTransaction represents the rejection of the creation of a StopLoss Order.
    """
    id: Optional[StrictStr] = Field(None, description="The Transaction's Identifier.")
    time: Optional[StrictStr] = Field(None, description="The date/time when the Transaction was created.")
    user_id: Optional[StrictInt] = Field(None, alias="userID", description="The ID of the user that initiated the creation of the Transaction.")
    account_id: Optional[StrictStr] = Field(None, alias="accountID", description="The ID of the Account the Transaction was created for.")
    batch_id: Optional[StrictStr] = Field(None, alias="batchID", description="The ID of the \"batch\" that the Transaction belongs to. Transactions in the same batch are applied to the Account simultaneously.")
    request_id: Optional[StrictStr] = Field(None, alias="requestID", description="The Request ID of the request which generated the transaction.")
    type: Optional[StrictStr] = Field(None, description="The Type of the Transaction. Always set to \"STOP_LOSS_ORDER_REJECT\" in a StopLossOrderRejectTransaction.")
    trade_id: Optional[StrictStr] = Field(None, alias="tradeID", description="The ID of the Trade to close when the price threshold is breached.")
    client_trade_id: Optional[StrictStr] = Field(None, alias="clientTradeID", description="The client ID of the Trade to be closed when the price threshold is breached.")
    price: Optional[StrictStr] = Field(None, description="The price threshold specified for the Stop Loss Order. If the guaranteed flag is false, the associated Trade will be closed by a market price that is equal to or worse than this threshold. If the flag is true the associated Trade will be closed at this price.")
    distance: Optional[StrictStr] = Field(None, description="Specifies the distance (in price units) from the Account's current price to use as the Stop Loss Order price. If the Trade is short the Instrument's bid price is used, and for long Trades the ask is used.")
    time_in_force: Optional[StrictStr] = Field(None, alias="timeInForce", description="The time-in-force requested for the StopLoss Order. Restricted to \"GTC\", \"GFD\" and \"GTD\" for StopLoss Orders.")
    gtd_time: Optional[StrictStr] = Field(None, alias="gtdTime", description="The date/time when the StopLoss Order will be cancelled if its timeInForce is \"GTD\".")
    trigger_condition: Optional[StrictStr] = Field(None, alias="triggerCondition", description="Specification of which price component should be used when determining if an Order should be triggered and filled. This allows Orders to be triggered based on the bid, ask, mid, default (ask for buy, bid for sell) or inverse (ask for sell, bid for buy) price depending on the desired behaviour. Orders are always filled using their default price component. This feature is only provided through the REST API. Clients who choose to specify a non-default trigger condition will not see it reflected in any of OANDA's proprietary or partner trading platforms, their transaction history or their account statements. OANDA platforms always assume that an Order's trigger condition is set to the default value when indicating the distance from an Order's trigger price, and will always provide the default trigger condition when creating or modifying an Order. A special restriction applies when creating a guaranteed Stop Loss Order. In this case the TriggerCondition value must either be \"DEFAULT\", or the \"natural\" trigger side \"DEFAULT\" results in. So for a Stop Loss Order for a long trade valid values are \"DEFAULT\" and \"BID\", and for short trades \"DEFAULT\" and \"ASK\" are valid.")
    guaranteed: Optional[StrictBool] = Field(None, description="Flag indicating that the Stop Loss Order is guaranteed. The default value depends on the GuaranteedStopLossOrderMode of the account, if it is REQUIRED, the default will be true, for DISABLED or ENABLED the default is false.")
    reason: Optional[StrictStr] = Field(None, description="The reason that the Stop Loss Order was initiated")
    client_extensions: Optional[ClientExtensions] = Field(None, alias="clientExtensions")
    order_fill_transaction_id: Optional[StrictStr] = Field(None, alias="orderFillTransactionID", description="The ID of the OrderFill Transaction that caused this Order to be created (only provided if this Order was created automatically when another Order was filled).")
    intended_replaces_order_id: Optional[StrictStr] = Field(None, alias="intendedReplacesOrderID", description="The ID of the Order that this Order was intended to replace (only provided if this Order was intended to replace an existing Order).")
    reject_reason: Optional[StrictStr] = Field(None, alias="rejectReason", description="The reason that the Reject Transaction was created")
    additional_properties: Dict[str, Any] = {}
    __properties = ["id", "time", "userID", "accountID", "batchID", "requestID", "type", "tradeID", "clientTradeID", "price", "distance", "timeInForce", "gtdTime", "triggerCondition", "guaranteed", "reason", "clientExtensions", "orderFillTransactionID", "intendedReplacesOrderID", "rejectReason"]

    @validator('type')
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('CREATE', 'CLOSE', 'REOPEN', 'CLIENT_CONFIGURE', 'CLIENT_CONFIGURE_REJECT', 'TRANSFER_FUNDS', 'TRANSFER_FUNDS_REJECT', 'MARKET_ORDER', 'MARKET_ORDER_REJECT', 'FIXED_PRICE_ORDER', 'LIMIT_ORDER', 'LIMIT_ORDER_REJECT', 'STOP_ORDER', 'STOP_ORDER_REJECT', 'MARKET_IF_TOUCHED_ORDER', 'MARKET_IF_TOUCHED_ORDER_REJECT', 'TAKE_PROFIT_ORDER', 'TAKE_PROFIT_ORDER_REJECT', 'STOP_LOSS_ORDER', 'STOP_LOSS_ORDER_REJECT', 'TRAILING_STOP_LOSS_ORDER', 'TRAILING_STOP_LOSS_ORDER_REJECT', 'ORDER_FILL', 'ORDER_CANCEL', 'ORDER_CANCEL_REJECT', 'ORDER_CLIENT_EXTENSIONS_MODIFY', 'ORDER_CLIENT_EXTENSIONS_MODIFY_REJECT', 'TRADE_CLIENT_EXTENSIONS_MODIFY', 'TRADE_CLIENT_EXTENSIONS_MODIFY_REJECT', 'MARGIN_CALL_ENTER', 'MARGIN_CALL_EXTEND', 'MARGIN_CALL_EXIT', 'DELAYED_TRADE_CLOSURE', 'DAILY_FINANCING', 'RESET_RESETTABLE_PL'):
            raise ValueError("must be one of enum values ('CREATE', 'CLOSE', 'REOPEN', 'CLIENT_CONFIGURE', 'CLIENT_CONFIGURE_REJECT', 'TRANSFER_FUNDS', 'TRANSFER_FUNDS_REJECT', 'MARKET_ORDER', 'MARKET_ORDER_REJECT', 'FIXED_PRICE_ORDER', 'LIMIT_ORDER', 'LIMIT_ORDER_REJECT', 'STOP_ORDER', 'STOP_ORDER_REJECT', 'MARKET_IF_TOUCHED_ORDER', 'MARKET_IF_TOUCHED_ORDER_REJECT', 'TAKE_PROFIT_ORDER', 'TAKE_PROFIT_ORDER_REJECT', 'STOP_LOSS_ORDER', 'STOP_LOSS_ORDER_REJECT', 'TRAILING_STOP_LOSS_ORDER', 'TRAILING_STOP_LOSS_ORDER_REJECT', 'ORDER_FILL', 'ORDER_CANCEL', 'ORDER_CANCEL_REJECT', 'ORDER_CLIENT_EXTENSIONS_MODIFY', 'ORDER_CLIENT_EXTENSIONS_MODIFY_REJECT', 'TRADE_CLIENT_EXTENSIONS_MODIFY', 'TRADE_CLIENT_EXTENSIONS_MODIFY_REJECT', 'MARGIN_CALL_ENTER', 'MARGIN_CALL_EXTEND', 'MARGIN_CALL_EXIT', 'DELAYED_TRADE_CLOSURE', 'DAILY_FINANCING', 'RESET_RESETTABLE_PL')")
        return value

    @validator('time_in_force')
    def time_in_force_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('GTC', 'GTD', 'GFD', 'FOK', 'IOC'):
            raise ValueError("must be one of enum values ('GTC', 'GTD', 'GFD', 'FOK', 'IOC')")
        return value

    @validator('trigger_condition')
    def trigger_condition_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('DEFAULT', 'INVERSE', 'BID', 'ASK', 'MID'):
            raise ValueError("must be one of enum values ('DEFAULT', 'INVERSE', 'BID', 'ASK', 'MID')")
        return value

    @validator('reason')
    def reason_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('CLIENT_ORDER', 'REPLACEMENT', 'ON_FILL'):
            raise ValueError("must be one of enum values ('CLIENT_ORDER', 'REPLACEMENT', 'ON_FILL')")
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
        validate_assignment = __debug__

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> "StopLossOrderRejectTransaction":
        """Create an instance of StopLossOrderRejectTransaction from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "additional_properties"
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of client_extensions
        if self.client_extensions:
            _dict['clientExtensions'] = self.client_extensions.to_dict()
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> StopLossOrderRejectTransaction:
        """Create an instance of StopLossOrderRejectTransaction from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return StopLossOrderRejectTransaction.parse_obj(obj)

        _obj = StopLossOrderRejectTransaction.parse_obj({
            "id": obj.get("id"),
            "time": obj.get("time"),
            "user_id": obj.get("userID"),
            "account_id": obj.get("accountID"),
            "batch_id": obj.get("batchID"),
            "request_id": obj.get("requestID"),
            "type": obj.get("type"),
            "trade_id": obj.get("tradeID"),
            "client_trade_id": obj.get("clientTradeID"),
            "price": obj.get("price"),
            "distance": obj.get("distance"),
            "time_in_force": obj.get("timeInForce"),
            "gtd_time": obj.get("gtdTime"),
            "trigger_condition": obj.get("triggerCondition"),
            "guaranteed": obj.get("guaranteed"),
            "reason": obj.get("reason"),
            "client_extensions": ClientExtensions.from_dict(obj.get("clientExtensions")) if obj.get("clientExtensions") is not None else None,
            "order_fill_transaction_id": obj.get("orderFillTransactionID"),
            "intended_replaces_order_id": obj.get("intendedReplacesOrderID"),
            "reject_reason": obj.get("rejectReason")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj


