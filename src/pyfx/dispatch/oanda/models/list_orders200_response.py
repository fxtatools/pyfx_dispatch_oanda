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
from pyfx.dispatch.oanda.models.order import Order

class ListOrders200Response(BaseModel):
    """
    ListOrders200Response
    """
    orders: Optional[conlist(Order)] = Field(None, description="The list of Order detail objects")
    last_transaction_id: Optional[StrictStr] = Field(None, alias="lastTransactionID", description="The ID of the most recent Transaction created for the Account")
    additional_properties: Dict[str, Any] = {}
    __properties = ["orders", "lastTransactionID"]

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
    def from_json(cls, json_str: str) -> "ListOrders200Response":
        """Create an instance of ListOrders200Response from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "additional_properties"
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in orders (list)
        _items = []
        if self.orders:
            for _item in self.orders:
                if _item:
                    _items.append(_item.to_dict())
            _dict['orders'] = _items
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ListOrders200Response:
        """Create an instance of ListOrders200Response from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ListOrders200Response.parse_obj(obj)

        _obj = ListOrders200Response.parse_obj({
            "orders": [Order.from_dict(_item) for _item in obj.get("orders")] if obj.get("orders") is not None else None,
            "last_transaction_id": obj.get("lastTransactionID")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj


