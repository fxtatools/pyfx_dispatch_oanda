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
from pydantic import BaseModel, Field, StrictStr, conlist
from pyfx.dispatch.oanda.models.trade_client_extensions_modify_transaction import TradeClientExtensionsModifyTransaction

class SetTradeClientExtensions200Response(BaseModel):
    """
    SetTradeClientExtensions200Response
    """
    trade_client_extensions_modify_transaction: Optional[TradeClientExtensionsModifyTransaction] = Field(None, alias="tradeClientExtensionsModifyTransaction")
    related_transaction_ids: Optional[conlist(StrictStr)] = Field(None, alias="relatedTransactionIDs", description="The IDs of all Transactions that were created while satisfying the request.")
    last_transaction_id: Optional[StrictStr] = Field(None, alias="lastTransactionID", description="The ID of the most recent Transaction created for the Account")
    additional_properties: Dict[str, Any] = {}
    __properties = ["tradeClientExtensionsModifyTransaction", "relatedTransactionIDs", "lastTransactionID"]

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
    def from_json(cls, json_str: str) -> "SetTradeClientExtensions200Response":
        """Create an instance of SetTradeClientExtensions200Response from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "additional_properties"
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of trade_client_extensions_modify_transaction
        if self.trade_client_extensions_modify_transaction:
            _dict['tradeClientExtensionsModifyTransaction'] = self.trade_client_extensions_modify_transaction.to_dict()
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SetTradeClientExtensions200Response:
        """Create an instance of SetTradeClientExtensions200Response from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SetTradeClientExtensions200Response.parse_obj(obj)

        _obj = SetTradeClientExtensions200Response.parse_obj({
            "trade_client_extensions_modify_transaction": TradeClientExtensionsModifyTransaction.from_dict(obj.get("tradeClientExtensionsModifyTransaction")) if obj.get("tradeClientExtensionsModifyTransaction") is not None else None,
            "related_transaction_ids": obj.get("relatedTransactionIDs"),
            "last_transaction_id": obj.get("lastTransactionID")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj


