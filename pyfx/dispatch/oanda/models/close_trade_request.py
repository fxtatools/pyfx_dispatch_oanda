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
from pydantic import BaseModel, Field, StrictStr

class CloseTradeRequest(BaseModel):
    """
    CloseTradeRequest
    """
    units: Optional[StrictStr] = Field(None, description="Indication of how much of the Trade to close. Either the string \"ALL\" (indicating that all of the Trade should be closed), or a DecimalNumber representing the number of units of the open Trade to Close using a TradeClose MarketOrder. The units specified must always be positive, and the magnitude of the value cannot exceed the magnitude of the Trade's open units.")
    additional_properties: Dict[str, Any] = {}
    __properties = ["units"]

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
    def from_json(cls, json_str: str) -> CloseTradeRequest:
        """Create an instance of CloseTradeRequest from a JSON string"""
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
    def from_dict(cls, obj: dict) -> CloseTradeRequest:
        """Create an instance of CloseTradeRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CloseTradeRequest.parse_obj(obj)

        _obj = CloseTradeRequest.parse_obj({
            "units": obj.get("units")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj


