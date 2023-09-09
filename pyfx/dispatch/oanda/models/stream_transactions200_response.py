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
from pydantic import BaseModel
from pyfx.dispatch.oanda.models.transaction import Transaction
from pyfx.dispatch.oanda.models.transaction_heartbeat import TransactionHeartbeat

class StreamTransactions200Response(BaseModel):
    """
    The response body for the Transaction Stream uses chunked transfer encoding.  Each chunk contains Transaction and/or TransactionHeartbeat objects encoded as JSON.  Each JSON object is serialized into a single line of text, and multiple objects found in the same chunk are separated by newlines. TransactionHeartbeats are sent every 5 seconds.
    """
    transaction: Optional[Transaction] = None
    heartbeat: Optional[TransactionHeartbeat] = None
    additional_properties: Dict[str, Any] = {}
    __properties = ["transaction", "heartbeat"]

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
    def from_json(cls, json_str: str) -> StreamTransactions200Response:
        """Create an instance of StreamTransactions200Response from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "additional_properties"
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of transaction
        if self.transaction:
            _dict['transaction'] = self.transaction.to_dict()
        # override the default output from pydantic by calling `to_dict()` of heartbeat
        if self.heartbeat:
            _dict['heartbeat'] = self.heartbeat.to_dict()
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> StreamTransactions200Response:
        """Create an instance of StreamTransactions200Response from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return StreamTransactions200Response.parse_obj(obj)

        _obj = StreamTransactions200Response.parse_obj({
            "transaction": Transaction.from_dict(obj.get("transaction")) if obj.get("transaction") is not None else None,
            "heartbeat": TransactionHeartbeat.from_dict(obj.get("heartbeat")) if obj.get("heartbeat") is not None else None
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj


