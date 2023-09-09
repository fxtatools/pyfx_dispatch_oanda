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

class MT4TransactionHeartbeat(BaseModel):
    """
    A TransactionHeartbeat object is injected into the Transaction stream to ensure that the HTTP connection remains active.
    """
    type: Optional[StrictStr] = Field(None, description="The string \"HEARTBEAT\"")
    time: Optional[StrictStr] = Field(None, description="The date/time when the TransactionHeartbeat was created.")
    additional_properties: Dict[str, Any] = {}
    __properties = ["type", "time"]

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
    def from_json(cls, json_str: str) -> MT4TransactionHeartbeat:
        """Create an instance of MT4TransactionHeartbeat from a JSON string"""
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
    def from_dict(cls, obj: dict) -> MT4TransactionHeartbeat:
        """Create an instance of MT4TransactionHeartbeat from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return MT4TransactionHeartbeat.parse_obj(obj)

        _obj = MT4TransactionHeartbeat.parse_obj({
            "type": obj.get("type"),
            "time": obj.get("time")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj


