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
from pydantic import BaseModel, Field, StrictInt, StrictStr

class UserInfo(BaseModel):
    """
    A representation of user information, as provided to the user themself.
    """
    username: Optional[StrictStr] = Field(None, description="The user-provided username.")
    user_id: Optional[StrictInt] = Field(None, alias="userID", description="The user's OANDA-assigned user ID.")
    country: Optional[StrictStr] = Field(None, description="The country that the user is based in.")
    email_address: Optional[StrictStr] = Field(None, alias="emailAddress", description="The user's email address.")
    additional_properties: Dict[str, Any] = {}
    __properties = ["username", "userID", "country", "emailAddress"]

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
    def from_json(cls, json_str: str) -> UserInfo:
        """Create an instance of UserInfo from a JSON string"""
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
    def from_dict(cls, obj: dict) -> UserInfo:
        """Create an instance of UserInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return UserInfo.parse_obj(obj)

        _obj = UserInfo.parse_obj({
            "username": obj.get("username"),
            "user_id": obj.get("userID"),
            "country": obj.get("country"),
            "email_address": obj.get("emailAddress")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj


