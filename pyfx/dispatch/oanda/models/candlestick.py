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
from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr
from pyfx.dispatch.oanda.models.candlestick_data import CandlestickData

class Candlestick(BaseModel):
    """
    The Candlestick representation
    """
    time: Optional[StrictStr] = Field(None, description="The start time of the candlestick")
    bid: Optional[CandlestickData] = None
    ask: Optional[CandlestickData] = None
    mid: Optional[CandlestickData] = None
    volume: Optional[StrictInt] = Field(None, description="The number of prices created during the time-range represented by the candlestick.")
    complete: Optional[StrictBool] = Field(None, description="A flag indicating if the candlestick is complete. A complete candlestick is one whose ending time is not in the future.")
    additional_properties: Dict[str, Any] = {}
    __properties = ["time", "bid", "ask", "mid", "volume", "complete"]

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
    def from_json(cls, json_str: str) -> Candlestick:
        """Create an instance of Candlestick from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "additional_properties"
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of bid
        if self.bid:
            _dict['bid'] = self.bid.to_dict()
        # override the default output from pydantic by calling `to_dict()` of ask
        if self.ask:
            _dict['ask'] = self.ask.to_dict()
        # override the default output from pydantic by calling `to_dict()` of mid
        if self.mid:
            _dict['mid'] = self.mid.to_dict()
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Candlestick:
        """Create an instance of Candlestick from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Candlestick.parse_obj(obj)

        _obj = Candlestick.parse_obj({
            "time": obj.get("time"),
            "bid": CandlestickData.from_dict(obj.get("bid")) if obj.get("bid") is not None else None,
            "ask": CandlestickData.from_dict(obj.get("ask")) if obj.get("ask") is not None else None,
            "mid": CandlestickData.from_dict(obj.get("mid")) if obj.get("mid") is not None else None,
            "volume": obj.get("volume"),
            "complete": obj.get("complete")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj


