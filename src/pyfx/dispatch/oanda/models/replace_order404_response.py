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
from pyfx.dispatch.oanda.models.transaction import Transaction

class ReplaceOrder404Response(BaseModel):
    """
    ReplaceOrder404Response
    """
    order_cancel_reject_transaction: Optional[Transaction] = Field(None, alias="orderCancelRejectTransaction")
    related_transaction_ids: Optional[conlist(StrictStr)] = Field(None, alias="relatedTransactionIDs", description="The IDs of all Transactions that were created while satisfying the request. Only present if the Account exists.")
    last_transaction_id: Optional[StrictStr] = Field(None, alias="lastTransactionID", description="The ID of the most recent Transaction created for the Account. Only present if the Account exists.")
    error_code: Optional[StrictStr] = Field(None, alias="errorCode", description="The code of the error that has occurred. This field may not be returned for some errors.")
    error_message: Optional[StrictStr] = Field(None, alias="errorMessage", description="The human-readable description of the error that has occurred.")
    additional_properties: Dict[str, Any] = {}
    __properties = ["orderCancelRejectTransaction", "relatedTransactionIDs", "lastTransactionID", "errorCode", "errorMessage"]

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
    def from_json(cls, json_str: str) -> "ReplaceOrder404Response":
        """Create an instance of ReplaceOrder404Response from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "additional_properties"
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of order_cancel_reject_transaction
        if self.order_cancel_reject_transaction:
            _dict['orderCancelRejectTransaction'] = self.order_cancel_reject_transaction.to_dict()
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ReplaceOrder404Response:
        """Create an instance of ReplaceOrder404Response from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ReplaceOrder404Response.parse_obj(obj)

        _obj = ReplaceOrder404Response.parse_obj({
            "order_cancel_reject_transaction": Transaction.from_dict(obj.get("orderCancelRejectTransaction")) if obj.get("orderCancelRejectTransaction") is not None else None,
            "related_transaction_ids": obj.get("relatedTransactionIDs"),
            "last_transaction_id": obj.get("lastTransactionID"),
            "error_code": obj.get("errorCode"),
            "error_message": obj.get("errorMessage")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj


