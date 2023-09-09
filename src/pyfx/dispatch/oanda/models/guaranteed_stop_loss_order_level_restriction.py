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

class GuaranteedStopLossOrderLevelRestriction(BaseModel):
    """
    A GuaranteedStopLossOrderLevelRestriction represents the total position size that can exist within a given price window for Trades with guaranteed Stop Loss Orders attached for a specific Instrument.
    """
    volume: Optional[StrictStr] = Field(None, description="Applies to Trades with a guaranteed Stop Loss Order attached for the specified Instrument. This is the total allowed Trade volume that can exist within the priceRange based on the trigger prices of the guaranteed Stop Loss Orders.")
    price_range: Optional[StrictStr] = Field(None, alias="priceRange", description="The price range the volume applies to. This value is in price units.")
    additional_properties: Dict[str, Any] = {}
    __properties = ["volume", "priceRange"]

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
    def from_json(cls, json_str: str) -> GuaranteedStopLossOrderLevelRestriction:
        """Create an instance of GuaranteedStopLossOrderLevelRestriction from a JSON string"""
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
    def from_dict(cls, obj: dict) -> GuaranteedStopLossOrderLevelRestriction:
        """Create an instance of GuaranteedStopLossOrderLevelRestriction from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return GuaranteedStopLossOrderLevelRestriction.parse_obj(obj)

        _obj = GuaranteedStopLossOrderLevelRestriction.parse_obj({
            "volume": obj.get("volume"),
            "price_range": obj.get("priceRange")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj

