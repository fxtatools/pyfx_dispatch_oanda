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

class StopLossOrderTransaction(BaseModel):
    """
    A StopLossOrderTransaction represents the creation of a StopLoss Order in the user's Account.
    """
    id: Optional[StrictStr] = Field(None, description="The Transaction's Identifier.")
    time: Optional[StrictStr] = Field(None, description="The date/time when the Transaction was created.")
    user_id: Optional[StrictInt] = Field(None, alias="userID", description="The ID of the user that initiated the creation of the Transaction.")
    account_id: Optional[StrictStr] = Field(None, alias="accountID", description="The ID of the Account the Transaction was created for.")
    batch_id: Optional[StrictStr] = Field(None, alias="batchID", description="The ID of the \"batch\" that the Transaction belongs to. Transactions in the same batch are applied to the Account simultaneously.")
    request_id: Optional[StrictStr] = Field(None, alias="requestID", description="The Request ID of the request which generated the transaction.")
    type: Optional[StrictStr] = Field(None, description="The Type of the Transaction. Always set to \"STOP_LOSS_ORDER\" in a StopLossOrderTransaction.")
    trade_id: Optional[StrictStr] = Field(None, alias="tradeID", description="The ID of the Trade to close when the price threshold is breached.")
    client_trade_id: Optional[StrictStr] = Field(None, alias="clientTradeID", description="The client ID of the Trade to be closed when the price threshold is breached.")
    price: Optional[StrictStr] = Field(None, description="The price threshold specified for the Stop Loss Order. If the guaranteed flag is false, the associated Trade will be closed by a market price that is equal to or worse than this threshold. If the flag is true the associated Trade will be closed at this price.")
    distance: Optional[StrictStr] = Field(None, description="Specifies the distance (in price units) from the Account's current price to use as the Stop Loss Order price. If the Trade is short the Instrument's bid price is used, and for long Trades the ask is used.")
    time_in_force: Optional[StrictStr] = Field(None, alias="timeInForce", description="The time-in-force requested for the StopLoss Order. Restricted to \"GTC\", \"GFD\" and \"GTD\" for StopLoss Orders.")
    gtd_time: Optional[StrictStr] = Field(None, alias="gtdTime", description="The date/time when the StopLoss Order will be cancelled if its timeInForce is \"GTD\".")
    trigger_condition: Optional[StrictStr] = Field(None, alias="triggerCondition", description="Specification of which price component should be used when determining if an Order should be triggered and filled. This allows Orders to be triggered based on the bid, ask, mid, default (ask for buy, bid for sell) or inverse (ask for sell, bid for buy) price depending on the desired behaviour. Orders are always filled using their default price component. This feature is only provided through the REST API. Clients who choose to specify a non-default trigger condition will not see it reflected in any of OANDA's proprietary or partner trading platforms, their transaction history or their account statements. OANDA platforms always assume that an Order's trigger condition is set to the default value when indicating the distance from an Order's trigger price, and will always provide the default trigger condition when creating or modifying an Order. A special restriction applies when creating a guaranteed Stop Loss Order. In this case the TriggerCondition value must either be \"DEFAULT\", or the \"natural\" trigger side \"DEFAULT\" results in. So for a Stop Loss Order for a long trade valid values are \"DEFAULT\" and \"BID\", and for short trades \"DEFAULT\" and \"ASK\" are valid.")
    guaranteed: Optional[StrictBool] = Field(None, description="Flag indicating that the Stop Loss Order is guaranteed. The default value depends on the GuaranteedStopLossOrderMode of the account, if it is REQUIRED, the default will be true, for DISABLED or ENABLED the default is false.")
    guaranteed_execution_premium: Optional[StrictStr] = Field(None, alias="guaranteedExecutionPremium", description="The fee that will be charged if the Stop Loss Order is guaranteed and the Order is filled at the guaranteed price. The value is determined at Order creation time. It is in price units and is charged for each unit of the Trade.")
    reason: Optional[StrictStr] = Field(None, description="The reason that the Stop Loss Order was initiated")
    client_extensions: Optional[ClientExtensions] = Field(None, alias="clientExtensions")
    order_fill_transaction_id: Optional[StrictStr] = Field(None, alias="orderFillTransactionID", description="The ID of the OrderFill Transaction that caused this Order to be created (only provided if this Order was created automatically when another Order was filled).")
    replaces_order_id: Optional[StrictStr] = Field(None, alias="replacesOrderID", description="The ID of the Order that this Order replaces (only provided if this Order replaces an existing Order).")
    cancelling_transaction_id: Optional[StrictStr] = Field(None, alias="cancellingTransactionID", description="The ID of the Transaction that cancels the replaced Order (only provided if this Order replaces an existing Order).")
    additional_properties: Dict[str, Any] = {}
    __properties = ["id", "time", "userID", "accountID", "batchID", "requestID", "type", "tradeID", "clientTradeID", "price", "distance", "timeInForce", "gtdTime", "triggerCondition", "guaranteed", "guaranteedExecutionPremium", "reason", "clientExtensions", "orderFillTransactionID", "replacesOrderID", "cancellingTransactionID"]

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
    def from_json(cls, json_str: str) -> StopLossOrderTransaction:
        """Create an instance of StopLossOrderTransaction from a JSON string"""
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
    def from_dict(cls, obj: dict) -> StopLossOrderTransaction:
        """Create an instance of StopLossOrderTransaction from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return StopLossOrderTransaction.parse_obj(obj)

        _obj = StopLossOrderTransaction.parse_obj({
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
            "guaranteed_execution_premium": obj.get("guaranteedExecutionPremium"),
            "reason": obj.get("reason"),
            "client_extensions": ClientExtensions.from_dict(obj.get("clientExtensions")) if obj.get("clientExtensions") is not None else None,
            "order_fill_transaction_id": obj.get("orderFillTransactionID"),
            "replaces_order_id": obj.get("replacesOrderID"),
            "cancelling_transaction_id": obj.get("cancellingTransactionID")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj


