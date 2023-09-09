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
from pydantic import BaseModel, Field
from pyfx.dispatch.oanda.models.units_available_details import UnitsAvailableDetails

class UnitsAvailable(BaseModel):
    """
    Representation of how many units of an Instrument are available to be traded by an Order depending on its postionFill option.
    """
    default: Optional[UnitsAvailableDetails] = None
    reduce_first: Optional[UnitsAvailableDetails] = Field(None, alias="reduceFirst")
    reduce_only: Optional[UnitsAvailableDetails] = Field(None, alias="reduceOnly")
    open_only: Optional[UnitsAvailableDetails] = Field(None, alias="openOnly")
    additional_properties: Dict[str, Any] = {}
    __properties = ["default", "reduceFirst", "reduceOnly", "openOnly"]

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
    def from_json(cls, json_str: str) -> UnitsAvailable:
        """Create an instance of UnitsAvailable from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "additional_properties"
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of default
        if self.default:
            _dict['default'] = self.default.to_dict()
        # override the default output from pydantic by calling `to_dict()` of reduce_first
        if self.reduce_first:
            _dict['reduceFirst'] = self.reduce_first.to_dict()
        # override the default output from pydantic by calling `to_dict()` of reduce_only
        if self.reduce_only:
            _dict['reduceOnly'] = self.reduce_only.to_dict()
        # override the default output from pydantic by calling `to_dict()` of open_only
        if self.open_only:
            _dict['openOnly'] = self.open_only.to_dict()
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> UnitsAvailable:
        """Create an instance of UnitsAvailable from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return UnitsAvailable.parse_obj(obj)

        _obj = UnitsAvailable.parse_obj({
            "default": UnitsAvailableDetails.from_dict(obj.get("default")) if obj.get("default") is not None else None,
            "reduce_first": UnitsAvailableDetails.from_dict(obj.get("reduceFirst")) if obj.get("reduceFirst") is not None else None,
            "reduce_only": UnitsAvailableDetails.from_dict(obj.get("reduceOnly")) if obj.get("reduceOnly") is not None else None,
            "open_only": UnitsAvailableDetails.from_dict(obj.get("openOnly")) if obj.get("openOnly") is not None else None
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj


