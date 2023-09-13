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


from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, StrictInt, StrictStr, conlist, validator
from pyfx.dispatch.oanda.models.client_price import ClientPrice
from pyfx.dispatch.oanda.models.trade_open import TradeOpen
from pyfx.dispatch.oanda.models.trade_reduce import TradeReduce

class OrderFillTransaction(BaseModel):
    """
    An OrderFillTransaction represents the filling of an Order in the client's Account.
    """
    id: Optional[StrictStr] = Field(None, description="The Transaction's Identifier.")
    time: Optional[StrictStr] = Field(None, description="The date/time when the Transaction was created.")
    user_id: Optional[StrictInt] = Field(None, alias="userID", description="The ID of the user that initiated the creation of the Transaction.")
    account_id: Optional[StrictStr] = Field(None, alias="accountID", description="The ID of the Account the Transaction was created for.")
    batch_id: Optional[StrictStr] = Field(None, alias="batchID", description="The ID of the \"batch\" that the Transaction belongs to. Transactions in the same batch are applied to the Account simultaneously.")
    request_id: Optional[StrictStr] = Field(None, alias="requestID", description="The Request ID of the request which generated the transaction.")
    type: Optional[StrictStr] = Field(None, description="The Type of the Transaction. Always set to \"ORDER_FILL\" for an OrderFillTransaction.")
    order_id: Optional[StrictStr] = Field(None, alias="orderID", description="The ID of the Order filled.")
    client_order_id: Optional[StrictStr] = Field(None, alias="clientOrderID", description="The client Order ID of the Order filled (only provided if the client has assigned one).")
    instrument: Optional[StrictStr] = Field(None, description="The name of the filled Order's instrument.")
    units: Optional[StrictStr] = Field(None, description="The number of units filled by the OrderFill.")
    gain_quote_home_conversion_factor: Optional[StrictStr] = Field(None, alias="gainQuoteHomeConversionFactor", description="This is the conversion factor in effect for the Account at the time of the OrderFill for converting any gains realized in Instrument quote units into units of the Account's home currency.")
    loss_quote_home_conversion_factor: Optional[StrictStr] = Field(None, alias="lossQuoteHomeConversionFactor", description="This is the conversion factor in effect for the Account at the time of the OrderFill for converting any losses realized in Instrument quote units into units of the Account's home currency.")
    price: Optional[StrictStr] = Field(None, description="This field is now deprecated and should no longer be used. The individual tradesClosed, tradeReduced and tradeOpened fields contain the exact/official price each unit was filled at.")
    full_vwap: Optional[StrictStr] = Field(None, alias="fullVWAP", description="The price that all of the units of the OrderFill should have been filled at, in the absence of guaranteed price execution. This factors in the Account's current ClientPrice, used liquidity and the units of the OrderFill only. If no Trades were closed with their price clamped for guaranteed stop loss enforcement, then this value will match the price fields of each Trade opened, closed, and reduced, and they will all be the exact same.")
    full_price: Optional[ClientPrice] = Field(None, alias="fullPrice")
    reason: Optional[StrictStr] = Field(None, description="The reason that an Order was filled")
    pl: Optional[StrictStr] = Field(None, description="The profit or loss incurred when the Order was filled.")
    financing: Optional[StrictStr] = Field(None, description="The financing paid or collected when the Order was filled.")
    commission: Optional[StrictStr] = Field(None, description="The commission charged in the Account's home currency as a result of filling the Order. The commission is always represented as a positive quantity of the Account's home currency, however it reduces the balance in the Account.")
    guaranteed_execution_fee: Optional[StrictStr] = Field(None, alias="guaranteedExecutionFee", description="The total guaranteed execution fees charged for all Trades opened, closed or reduced with guaranteed Stop Loss Orders.")
    account_balance: Optional[StrictStr] = Field(None, alias="accountBalance", description="The Account's balance after the Order was filled.")
    trade_opened: Optional[TradeOpen] = Field(None, alias="tradeOpened")
    trades_closed: Optional[conlist(TradeReduce)] = Field(None, alias="tradesClosed", description="The Trades that were closed when the Order was filled (only provided if filling the Order resulted in a closing open Trades).")
    trade_reduced: Optional[TradeReduce] = Field(None, alias="tradeReduced")
    half_spread_cost: Optional[StrictStr] = Field(None, alias="halfSpreadCost", description="The half spread cost for the OrderFill, which is the sum of the halfSpreadCost values in the tradeOpened, tradesClosed and tradeReduced fields. This can be a positive or negative value and is represented in the home currency of the Account.")
    additional_properties: Dict[str, Any] = {}
    __properties = ["id", "time", "userID", "accountID", "batchID", "requestID", "type", "orderID", "clientOrderID", "instrument", "units", "gainQuoteHomeConversionFactor", "lossQuoteHomeConversionFactor", "price", "fullVWAP", "fullPrice", "reason", "pl", "financing", "commission", "guaranteedExecutionFee", "accountBalance", "tradeOpened", "tradesClosed", "tradeReduced", "halfSpreadCost"]

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

        if value not in ('LIMIT_ORDER', 'STOP_ORDER', 'MARKET_IF_TOUCHED_ORDER', 'TAKE_PROFIT_ORDER', 'STOP_LOSS_ORDER', 'TRAILING_STOP_LOSS_ORDER', 'MARKET_ORDER', 'MARKET_ORDER_TRADE_CLOSE', 'MARKET_ORDER_POSITION_CLOSEOUT', 'MARKET_ORDER_MARGIN_CLOSEOUT', 'MARKET_ORDER_DELAYED_TRADE_CLOSE'):
            raise ValueError("must be one of enum values ('LIMIT_ORDER', 'STOP_ORDER', 'MARKET_IF_TOUCHED_ORDER', 'TAKE_PROFIT_ORDER', 'STOP_LOSS_ORDER', 'TRAILING_STOP_LOSS_ORDER', 'MARKET_ORDER', 'MARKET_ORDER_TRADE_CLOSE', 'MARKET_ORDER_POSITION_CLOSEOUT', 'MARKET_ORDER_MARGIN_CLOSEOUT', 'MARKET_ORDER_DELAYED_TRADE_CLOSE')")
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
    def from_json(cls, json_str: str) -> "OrderFillTransaction":
        """Create an instance of OrderFillTransaction from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "additional_properties"
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of full_price
        if self.full_price:
            _dict['fullPrice'] = self.full_price.to_dict()
        # override the default output from pydantic by calling `to_dict()` of trade_opened
        if self.trade_opened:
            _dict['tradeOpened'] = self.trade_opened.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in trades_closed (list)
        _items = []
        if self.trades_closed:
            for _item in self.trades_closed:
                if _item:
                    _items.append(_item.to_dict())
            _dict['tradesClosed'] = _items
        # override the default output from pydantic by calling `to_dict()` of trade_reduced
        if self.trade_reduced:
            _dict['tradeReduced'] = self.trade_reduced.to_dict()
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> OrderFillTransaction:
        """Create an instance of OrderFillTransaction from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return OrderFillTransaction.parse_obj(obj)

        _obj = OrderFillTransaction.parse_obj({
            "id": obj.get("id"),
            "time": obj.get("time"),
            "user_id": obj.get("userID"),
            "account_id": obj.get("accountID"),
            "batch_id": obj.get("batchID"),
            "request_id": obj.get("requestID"),
            "type": obj.get("type"),
            "order_id": obj.get("orderID"),
            "client_order_id": obj.get("clientOrderID"),
            "instrument": obj.get("instrument"),
            "units": obj.get("units"),
            "gain_quote_home_conversion_factor": obj.get("gainQuoteHomeConversionFactor"),
            "loss_quote_home_conversion_factor": obj.get("lossQuoteHomeConversionFactor"),
            "price": obj.get("price"),
            "full_vwap": obj.get("fullVWAP"),
            "full_price": ClientPrice.from_dict(obj.get("fullPrice")) if obj.get("fullPrice") is not None else None,
            "reason": obj.get("reason"),
            "pl": obj.get("pl"),
            "financing": obj.get("financing"),
            "commission": obj.get("commission"),
            "guaranteed_execution_fee": obj.get("guaranteedExecutionFee"),
            "account_balance": obj.get("accountBalance"),
            "trade_opened": TradeOpen.from_dict(obj.get("tradeOpened")) if obj.get("tradeOpened") is not None else None,
            "trades_closed": [TradeReduce.from_dict(_item) for _item in obj.get("tradesClosed")] if obj.get("tradesClosed") is not None else None,
            "trade_reduced": TradeReduce.from_dict(obj.get("tradeReduced")) if obj.get("tradeReduced") is not None else None,
            "half_spread_cost": obj.get("halfSpreadCost")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj


