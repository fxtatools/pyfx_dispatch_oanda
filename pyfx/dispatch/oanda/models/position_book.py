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
from pyfx.dispatch.oanda.models.position_book_bucket import PositionBookBucket

class PositionBook(BaseModel):
    """
    The representation of an instrument's position book at a point in time
    """
    instrument: Optional[StrictStr] = Field(None, description="The position book's instrument")
    time: Optional[StrictStr] = Field(None, description="The time when the position book snapshot was created")
    price: Optional[StrictStr] = Field(None, description="The price (midpoint) for the position book's instrument at the time of the position book snapshot")
    bucket_width: Optional[StrictStr] = Field(None, alias="bucketWidth", description="The price width for each bucket. Each bucket covers the price range from the bucket's price to the bucket's price + bucketWidth.")
    buckets: Optional[conlist(PositionBookBucket)] = Field(None, description="The partitioned position book, divided into buckets using a default bucket width. These buckets are only provided for price ranges which actually contain order or position data.")
    additional_properties: Dict[str, Any] = {}
    __properties = ["instrument", "time", "price", "bucketWidth", "buckets"]

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
    def from_json(cls, json_str: str) -> PositionBook:
        """Create an instance of PositionBook from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "additional_properties"
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in buckets (list)
        _items = []
        if self.buckets:
            for _item in self.buckets:
                if _item:
                    _items.append(_item.to_dict())
            _dict['buckets'] = _items
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PositionBook:
        """Create an instance of PositionBook from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PositionBook.parse_obj(obj)

        _obj = PositionBook.parse_obj({
            "instrument": obj.get("instrument"),
            "time": obj.get("time"),
            "price": obj.get("price"),
            "bucket_width": obj.get("bucketWidth"),
            "buckets": [PositionBookBucket.from_dict(_item) for _item in obj.get("buckets")] if obj.get("buckets") is not None else None
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj


