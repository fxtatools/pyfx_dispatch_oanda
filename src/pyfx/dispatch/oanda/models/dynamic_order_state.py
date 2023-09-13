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
from pydantic import BaseModel, Field, StrictBool, StrictStr

class DynamicOrderState(BaseModel):
    """
    The dynamic state of an Order. This is only relevant to TrailingStopLoss Orders, as no other Order type has dynamic state.
    """
    id: Optional[StrictStr] = Field(None, description="The Order's ID.")
    trailing_stop_value: Optional[StrictStr] = Field(None, alias="trailingStopValue", description="The Order's calculated trailing stop value.")
    trigger_distance: Optional[StrictStr] = Field(None, alias="triggerDistance", description="The distance between the Trailing Stop Loss Order's trailingStopValue and the current Market Price. This represents the distance (in price units) of the Order from a triggering price. If the distance could not be determined, this value will not be set.")
    is_trigger_distance_exact: Optional[StrictBool] = Field(None, alias="isTriggerDistanceExact", description="True if an exact trigger distance could be calculated. If false, it means the provided trigger distance is a best estimate. If the distance could not be determined, this value will not be set.")
    additional_properties: Dict[str, Any] = {}
    __properties = ["id", "trailingStopValue", "triggerDistance", "isTriggerDistanceExact"]

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
    def from_json(cls, json_str: str) -> "DynamicOrderState":
        """Create an instance of DynamicOrderState from a JSON string"""
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
    def from_dict(cls, obj: dict) -> DynamicOrderState:
        """Create an instance of DynamicOrderState from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return DynamicOrderState.parse_obj(obj)

        _obj = DynamicOrderState.parse_obj({
            "id": obj.get("id"),
            "trailing_stop_value": obj.get("trailingStopValue"),
            "trigger_distance": obj.get("triggerDistance"),
            "is_trigger_distance_exact": obj.get("isTriggerDistanceExact")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj


