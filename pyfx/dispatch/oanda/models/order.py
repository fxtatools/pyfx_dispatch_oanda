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
from pydantic import BaseModel, Field, StrictStr, validator
from pyfx.dispatch.oanda.models.client_extensions import ClientExtensions

class Order(BaseModel):
    """
    The base Order definition specifies the properties that are common to all Orders.
    """
    id: Optional[StrictStr] = Field(None, description="The Order's identifier, unique within the Order's Account.")
    create_time: Optional[StrictStr] = Field(None, alias="createTime", description="The time when the Order was created.")
    state: Optional[StrictStr] = Field(None, description="The current state of the Order.")
    client_extensions: Optional[ClientExtensions] = Field(None, alias="clientExtensions")
    additional_properties: Dict[str, Any] = {}
    __properties = ["id", "createTime", "state", "clientExtensions"]

    @validator('state')
    def state_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('PENDING', 'FILLED', 'TRIGGERED', 'CANCELLED'):
            raise ValueError("must be one of enum values ('PENDING', 'FILLED', 'TRIGGERED', 'CANCELLED')")
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
    def from_json(cls, json_str: str) -> Order:
        """Create an instance of Order from a JSON string"""
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
    def from_dict(cls, obj: dict) -> Order:
        """Create an instance of Order from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Order.parse_obj(obj)

        _obj = Order.parse_obj({
            "id": obj.get("id"),
            "create_time": obj.get("createTime"),
            "state": obj.get("state"),
            "client_extensions": ClientExtensions.from_dict(obj.get("clientExtensions")) if obj.get("clientExtensions") is not None else None
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj


