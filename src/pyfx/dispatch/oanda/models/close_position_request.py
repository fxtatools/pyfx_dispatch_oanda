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
from pydantic import BaseModel, Field, StrictStr
from pyfx.dispatch.oanda.models.client_extensions import ClientExtensions

class ClosePositionRequest(BaseModel):
    """
    ClosePositionRequest
    """
    long_units: Optional[StrictStr] = Field(None, alias="longUnits", description="Indication of how much of the long Position to closeout. Either the string \"ALL\", the string \"NONE\", or a DecimalNumber representing how many units of the long position to close using a PositionCloseout MarketOrder. The units specified must always be positive.")
    long_client_extensions: Optional[ClientExtensions] = Field(None, alias="longClientExtensions")
    short_units: Optional[StrictStr] = Field(None, alias="shortUnits", description="Indication of how much of the short Position to closeout. Either the string \"ALL\", the string \"NONE\", or a DecimalNumber representing how many units of the short position to close using a PositionCloseout MarketOrder. The units specified must always be positive.")
    short_client_extensions: Optional[ClientExtensions] = Field(None, alias="shortClientExtensions")
    additional_properties: Dict[str, Any] = {}
    __properties = ["longUnits", "longClientExtensions", "shortUnits", "shortClientExtensions"]

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
    def from_json(cls, json_str: str) -> ClosePositionRequest:
        """Create an instance of ClosePositionRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "additional_properties"
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of long_client_extensions
        if self.long_client_extensions:
            _dict['longClientExtensions'] = self.long_client_extensions.to_dict()
        # override the default output from pydantic by calling `to_dict()` of short_client_extensions
        if self.short_client_extensions:
            _dict['shortClientExtensions'] = self.short_client_extensions.to_dict()
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ClosePositionRequest:
        """Create an instance of ClosePositionRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ClosePositionRequest.parse_obj(obj)

        _obj = ClosePositionRequest.parse_obj({
            "long_units": obj.get("longUnits"),
            "long_client_extensions": ClientExtensions.from_dict(obj.get("longClientExtensions")) if obj.get("longClientExtensions") is not None else None,
            "short_units": obj.get("shortUnits"),
            "short_client_extensions": ClientExtensions.from_dict(obj.get("shortClientExtensions")) if obj.get("shortClientExtensions") is not None else None
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj

