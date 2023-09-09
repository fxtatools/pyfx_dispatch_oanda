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

class ListTransactions200Response(BaseModel):
    """
    ListTransactions200Response
    """
    var_from: Optional[StrictStr] = Field(None, alias="from", description="The starting time provided in the request.")
    to: Optional[StrictStr] = Field(None, description="The ending time provided in the request.")
    page_size: Optional[StrictInt] = Field(None, alias="pageSize", description="The pageSize provided in the request")
    type: Optional[conlist(StrictStr)] = Field(None, description="The Transaction-type filter provided in the request")
    count: Optional[StrictInt] = Field(None, description="The number of Transactions that are contained in the pages returned")
    pages: Optional[conlist(StrictStr)] = Field(None, description="The list of URLs that represent idrange queries providing the data for each page in the query results")
    last_transaction_id: Optional[StrictStr] = Field(None, alias="lastTransactionID", description="The ID of the most recent Transaction created for the Account")
    additional_properties: Dict[str, Any] = {}
    __properties = ["from", "to", "pageSize", "type", "count", "pages", "lastTransactionID"]

    @validator('type')
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        for i in value:
            if i not in ('ORDER', 'FUNDING', 'ADMIN', 'CREATE', 'CLOSE', 'REOPEN', 'CLIENT_CONFIGURE', 'CLIENT_CONFIGURE_REJECT', 'TRANSFER_FUNDS', 'TRANSFER_FUNDS_REJECT', 'MARKET_ORDER', 'MARKET_ORDER_REJECT', 'LIMIT_ORDER', 'LIMIT_ORDER_REJECT', 'STOP_ORDER', 'STOP_ORDER_REJECT', 'MARKET_IF_TOUCHED_ORDER', 'MARKET_IF_TOUCHED_ORDER_REJECT', 'TAKE_PROFIT_ORDER', 'TAKE_PROFIT_ORDER_REJECT', 'STOP_LOSS_ORDER', 'STOP_LOSS_ORDER_REJECT', 'TRAILING_STOP_LOSS_ORDER', 'TRAILING_STOP_LOSS_ORDER_REJECT', 'ONE_CANCELS_ALL_ORDER', 'ONE_CANCELS_ALL_ORDER_REJECT', 'ONE_CANCELS_ALL_ORDER_TRIGGERED', 'ORDER_FILL', 'ORDER_CANCEL', 'ORDER_CANCEL_REJECT', 'ORDER_CLIENT_EXTENSIONS_MODIFY', 'ORDER_CLIENT_EXTENSIONS_MODIFY_REJECT', 'TRADE_CLIENT_EXTENSIONS_MODIFY', 'TRADE_CLIENT_EXTENSIONS_MODIFY_REJECT', 'MARGIN_CALL_ENTER', 'MARGIN_CALL_EXTEND', 'MARGIN_CALL_EXIT', 'DELAYED_TRADE_CLOSURE', 'DAILY_FINANCING', 'RESET_RESETTABLE_PL'):
                raise ValueError("each list item must be one of ('ORDER', 'FUNDING', 'ADMIN', 'CREATE', 'CLOSE', 'REOPEN', 'CLIENT_CONFIGURE', 'CLIENT_CONFIGURE_REJECT', 'TRANSFER_FUNDS', 'TRANSFER_FUNDS_REJECT', 'MARKET_ORDER', 'MARKET_ORDER_REJECT', 'LIMIT_ORDER', 'LIMIT_ORDER_REJECT', 'STOP_ORDER', 'STOP_ORDER_REJECT', 'MARKET_IF_TOUCHED_ORDER', 'MARKET_IF_TOUCHED_ORDER_REJECT', 'TAKE_PROFIT_ORDER', 'TAKE_PROFIT_ORDER_REJECT', 'STOP_LOSS_ORDER', 'STOP_LOSS_ORDER_REJECT', 'TRAILING_STOP_LOSS_ORDER', 'TRAILING_STOP_LOSS_ORDER_REJECT', 'ONE_CANCELS_ALL_ORDER', 'ONE_CANCELS_ALL_ORDER_REJECT', 'ONE_CANCELS_ALL_ORDER_TRIGGERED', 'ORDER_FILL', 'ORDER_CANCEL', 'ORDER_CANCEL_REJECT', 'ORDER_CLIENT_EXTENSIONS_MODIFY', 'ORDER_CLIENT_EXTENSIONS_MODIFY_REJECT', 'TRADE_CLIENT_EXTENSIONS_MODIFY', 'TRADE_CLIENT_EXTENSIONS_MODIFY_REJECT', 'MARGIN_CALL_ENTER', 'MARGIN_CALL_EXTEND', 'MARGIN_CALL_EXIT', 'DELAYED_TRADE_CLOSURE', 'DAILY_FINANCING', 'RESET_RESETTABLE_PL')")
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
    def from_json(cls, json_str: str) -> ListTransactions200Response:
        """Create an instance of ListTransactions200Response from a JSON string"""
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
    def from_dict(cls, obj: dict) -> ListTransactions200Response:
        """Create an instance of ListTransactions200Response from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ListTransactions200Response.parse_obj(obj)

        _obj = ListTransactions200Response.parse_obj({
            "var_from": obj.get("from"),
            "to": obj.get("to"),
            "page_size": obj.get("pageSize"),
            "type": obj.get("type"),
            "count": obj.get("count"),
            "pages": obj.get("pages"),
            "last_transaction_id": obj.get("lastTransactionID")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj

