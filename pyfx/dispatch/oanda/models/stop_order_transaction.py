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
from pyfx.dispatch.oanda.models.client_extensions import ClientExtensions
from pyfx.dispatch.oanda.models.stop_loss_details import StopLossDetails
from pyfx.dispatch.oanda.models.take_profit_details import TakeProfitDetails
from pyfx.dispatch.oanda.models.trailing_stop_loss_details import TrailingStopLossDetails

class StopOrderTransaction(BaseModel):
    """
    A StopOrderTransaction represents the creation of a Stop Order in the user's Account.
    """
    id: Optional[StrictStr] = Field(None, description="The Transaction's Identifier.")
    time: Optional[StrictStr] = Field(None, description="The date/time when the Transaction was created.")
    user_id: Optional[StrictInt] = Field(None, alias="userID", description="The ID of the user that initiated the creation of the Transaction.")
    account_id: Optional[StrictStr] = Field(None, alias="accountID", description="The ID of the Account the Transaction was created for.")
    batch_id: Optional[StrictStr] = Field(None, alias="batchID", description="The ID of the \"batch\" that the Transaction belongs to. Transactions in the same batch are applied to the Account simultaneously.")
    request_id: Optional[StrictStr] = Field(None, alias="requestID", description="The Request ID of the request which generated the transaction.")
    type: Optional[StrictStr] = Field(None, description="The Type of the Transaction. Always set to \"STOP_ORDER\" in a StopOrderTransaction.")
    instrument: Optional[StrictStr] = Field(None, description="The Stop Order's Instrument.")
    units: Optional[StrictStr] = Field(None, description="The quantity requested to be filled by the Stop Order. A posititive number of units results in a long Order, and a negative number of units results in a short Order.")
    price: Optional[StrictStr] = Field(None, description="The price threshold specified for the Stop Order. The Stop Order will only be filled by a market price that is equal to or worse than this price.")
    price_bound: Optional[StrictStr] = Field(None, alias="priceBound", description="The worst market price that may be used to fill this Stop Order. If the market gaps and crosses through both the price and the priceBound, the Stop Order will be cancelled instead of being filled.")
    time_in_force: Optional[StrictStr] = Field(None, alias="timeInForce", description="The time-in-force requested for the Stop Order.")
    gtd_time: Optional[StrictStr] = Field(None, alias="gtdTime", description="The date/time when the Stop Order will be cancelled if its timeInForce is \"GTD\".")
    position_fill: Optional[StrictStr] = Field(None, alias="positionFill", description="Specification of how Positions in the Account are modified when the Order is filled.")
    trigger_condition: Optional[StrictStr] = Field(None, alias="triggerCondition", description="Specification of which price component should be used when determining if an Order should be triggered and filled. This allows Orders to be triggered based on the bid, ask, mid, default (ask for buy, bid for sell) or inverse (ask for sell, bid for buy) price depending on the desired behaviour. Orders are always filled using their default price component. This feature is only provided through the REST API. Clients who choose to specify a non-default trigger condition will not see it reflected in any of OANDA's proprietary or partner trading platforms, their transaction history or their account statements. OANDA platforms always assume that an Order's trigger condition is set to the default value when indicating the distance from an Order's trigger price, and will always provide the default trigger condition when creating or modifying an Order. A special restriction applies when creating a guaranteed Stop Loss Order. In this case the TriggerCondition value must either be \"DEFAULT\", or the \"natural\" trigger side \"DEFAULT\" results in. So for a Stop Loss Order for a long trade valid values are \"DEFAULT\" and \"BID\", and for short trades \"DEFAULT\" and \"ASK\" are valid.")
    reason: Optional[StrictStr] = Field(None, description="The reason that the Stop Order was initiated")
    client_extensions: Optional[ClientExtensions] = Field(None, alias="clientExtensions")
    take_profit_on_fill: Optional[TakeProfitDetails] = Field(None, alias="takeProfitOnFill")
    stop_loss_on_fill: Optional[StopLossDetails] = Field(None, alias="stopLossOnFill")
    trailing_stop_loss_on_fill: Optional[TrailingStopLossDetails] = Field(None, alias="trailingStopLossOnFill")
    trade_client_extensions: Optional[ClientExtensions] = Field(None, alias="tradeClientExtensions")
    replaces_order_id: Optional[StrictStr] = Field(None, alias="replacesOrderID", description="The ID of the Order that this Order replaces (only provided if this Order replaces an existing Order).")
    cancelling_transaction_id: Optional[StrictStr] = Field(None, alias="cancellingTransactionID", description="The ID of the Transaction that cancels the replaced Order (only provided if this Order replaces an existing Order).")
    additional_properties: Dict[str, Any] = {}
    __properties = ["id", "time", "userID", "accountID", "batchID", "requestID", "type", "instrument", "units", "price", "priceBound", "timeInForce", "gtdTime", "positionFill", "triggerCondition", "reason", "clientExtensions", "takeProfitOnFill", "stopLossOnFill", "trailingStopLossOnFill", "tradeClientExtensions", "replacesOrderID", "cancellingTransactionID"]

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

    @validator('position_fill')
    def position_fill_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('OPEN_ONLY', 'REDUCE_FIRST', 'REDUCE_ONLY', 'DEFAULT'):
            raise ValueError("must be one of enum values ('OPEN_ONLY', 'REDUCE_FIRST', 'REDUCE_ONLY', 'DEFAULT')")
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

        if value not in ('CLIENT_ORDER', 'REPLACEMENT'):
            raise ValueError("must be one of enum values ('CLIENT_ORDER', 'REPLACEMENT')")
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
    def from_json(cls, json_str: str) -> StopOrderTransaction:
        """Create an instance of StopOrderTransaction from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of take_profit_on_fill
        if self.take_profit_on_fill:
            _dict['takeProfitOnFill'] = self.take_profit_on_fill.to_dict()
        # override the default output from pydantic by calling `to_dict()` of stop_loss_on_fill
        if self.stop_loss_on_fill:
            _dict['stopLossOnFill'] = self.stop_loss_on_fill.to_dict()
        # override the default output from pydantic by calling `to_dict()` of trailing_stop_loss_on_fill
        if self.trailing_stop_loss_on_fill:
            _dict['trailingStopLossOnFill'] = self.trailing_stop_loss_on_fill.to_dict()
        # override the default output from pydantic by calling `to_dict()` of trade_client_extensions
        if self.trade_client_extensions:
            _dict['tradeClientExtensions'] = self.trade_client_extensions.to_dict()
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> StopOrderTransaction:
        """Create an instance of StopOrderTransaction from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return StopOrderTransaction.parse_obj(obj)

        _obj = StopOrderTransaction.parse_obj({
            "id": obj.get("id"),
            "time": obj.get("time"),
            "user_id": obj.get("userID"),
            "account_id": obj.get("accountID"),
            "batch_id": obj.get("batchID"),
            "request_id": obj.get("requestID"),
            "type": obj.get("type"),
            "instrument": obj.get("instrument"),
            "units": obj.get("units"),
            "price": obj.get("price"),
            "price_bound": obj.get("priceBound"),
            "time_in_force": obj.get("timeInForce"),
            "gtd_time": obj.get("gtdTime"),
            "position_fill": obj.get("positionFill"),
            "trigger_condition": obj.get("triggerCondition"),
            "reason": obj.get("reason"),
            "client_extensions": ClientExtensions.from_dict(obj.get("clientExtensions")) if obj.get("clientExtensions") is not None else None,
            "take_profit_on_fill": TakeProfitDetails.from_dict(obj.get("takeProfitOnFill")) if obj.get("takeProfitOnFill") is not None else None,
            "stop_loss_on_fill": StopLossDetails.from_dict(obj.get("stopLossOnFill")) if obj.get("stopLossOnFill") is not None else None,
            "trailing_stop_loss_on_fill": TrailingStopLossDetails.from_dict(obj.get("trailingStopLossOnFill")) if obj.get("trailingStopLossOnFill") is not None else None,
            "trade_client_extensions": ClientExtensions.from_dict(obj.get("tradeClientExtensions")) if obj.get("tradeClientExtensions") is not None else None,
            "replaces_order_id": obj.get("replacesOrderID"),
            "cancelling_transaction_id": obj.get("cancellingTransactionID")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj


