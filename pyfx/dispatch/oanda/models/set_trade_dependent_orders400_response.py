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
from pyfx.dispatch.oanda.models.order_cancel_reject_transaction import OrderCancelRejectTransaction
from pyfx.dispatch.oanda.models.stop_loss_order_reject_transaction import StopLossOrderRejectTransaction
from pyfx.dispatch.oanda.models.take_profit_order_reject_transaction import TakeProfitOrderRejectTransaction
from pyfx.dispatch.oanda.models.trailing_stop_loss_order_reject_transaction import TrailingStopLossOrderRejectTransaction

class SetTradeDependentOrders400Response(BaseModel):
    """
    SetTradeDependentOrders400Response
    """
    take_profit_order_cancel_reject_transaction: Optional[OrderCancelRejectTransaction] = Field(None, alias="takeProfitOrderCancelRejectTransaction")
    take_profit_order_reject_transaction: Optional[TakeProfitOrderRejectTransaction] = Field(None, alias="takeProfitOrderRejectTransaction")
    stop_loss_order_cancel_reject_transaction: Optional[OrderCancelRejectTransaction] = Field(None, alias="stopLossOrderCancelRejectTransaction")
    stop_loss_order_reject_transaction: Optional[StopLossOrderRejectTransaction] = Field(None, alias="stopLossOrderRejectTransaction")
    trailing_stop_loss_order_cancel_reject_transaction: Optional[OrderCancelRejectTransaction] = Field(None, alias="trailingStopLossOrderCancelRejectTransaction")
    trailing_stop_loss_order_reject_transaction: Optional[TrailingStopLossOrderRejectTransaction] = Field(None, alias="trailingStopLossOrderRejectTransaction")
    last_transaction_id: Optional[StrictStr] = Field(None, alias="lastTransactionID", description="The ID of the most recent Transaction created for the Account.")
    related_transaction_ids: Optional[conlist(StrictStr)] = Field(None, alias="relatedTransactionIDs", description="The IDs of all Transactions that were created while satisfying the request.")
    error_code: Optional[StrictStr] = Field(None, alias="errorCode", description="The code of the error that has occurred. This field may not be returned for some errors.")
    error_message: Optional[StrictStr] = Field(None, alias="errorMessage", description="The human-readable description of the error that has occurred.")
    additional_properties: Dict[str, Any] = {}
    __properties = ["takeProfitOrderCancelRejectTransaction", "takeProfitOrderRejectTransaction", "stopLossOrderCancelRejectTransaction", "stopLossOrderRejectTransaction", "trailingStopLossOrderCancelRejectTransaction", "trailingStopLossOrderRejectTransaction", "lastTransactionID", "relatedTransactionIDs", "errorCode", "errorMessage"]

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
    def from_json(cls, json_str: str) -> SetTradeDependentOrders400Response:
        """Create an instance of SetTradeDependentOrders400Response from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "additional_properties"
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of take_profit_order_cancel_reject_transaction
        if self.take_profit_order_cancel_reject_transaction:
            _dict['takeProfitOrderCancelRejectTransaction'] = self.take_profit_order_cancel_reject_transaction.to_dict()
        # override the default output from pydantic by calling `to_dict()` of take_profit_order_reject_transaction
        if self.take_profit_order_reject_transaction:
            _dict['takeProfitOrderRejectTransaction'] = self.take_profit_order_reject_transaction.to_dict()
        # override the default output from pydantic by calling `to_dict()` of stop_loss_order_cancel_reject_transaction
        if self.stop_loss_order_cancel_reject_transaction:
            _dict['stopLossOrderCancelRejectTransaction'] = self.stop_loss_order_cancel_reject_transaction.to_dict()
        # override the default output from pydantic by calling `to_dict()` of stop_loss_order_reject_transaction
        if self.stop_loss_order_reject_transaction:
            _dict['stopLossOrderRejectTransaction'] = self.stop_loss_order_reject_transaction.to_dict()
        # override the default output from pydantic by calling `to_dict()` of trailing_stop_loss_order_cancel_reject_transaction
        if self.trailing_stop_loss_order_cancel_reject_transaction:
            _dict['trailingStopLossOrderCancelRejectTransaction'] = self.trailing_stop_loss_order_cancel_reject_transaction.to_dict()
        # override the default output from pydantic by calling `to_dict()` of trailing_stop_loss_order_reject_transaction
        if self.trailing_stop_loss_order_reject_transaction:
            _dict['trailingStopLossOrderRejectTransaction'] = self.trailing_stop_loss_order_reject_transaction.to_dict()
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SetTradeDependentOrders400Response:
        """Create an instance of SetTradeDependentOrders400Response from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SetTradeDependentOrders400Response.parse_obj(obj)

        _obj = SetTradeDependentOrders400Response.parse_obj({
            "take_profit_order_cancel_reject_transaction": OrderCancelRejectTransaction.from_dict(obj.get("takeProfitOrderCancelRejectTransaction")) if obj.get("takeProfitOrderCancelRejectTransaction") is not None else None,
            "take_profit_order_reject_transaction": TakeProfitOrderRejectTransaction.from_dict(obj.get("takeProfitOrderRejectTransaction")) if obj.get("takeProfitOrderRejectTransaction") is not None else None,
            "stop_loss_order_cancel_reject_transaction": OrderCancelRejectTransaction.from_dict(obj.get("stopLossOrderCancelRejectTransaction")) if obj.get("stopLossOrderCancelRejectTransaction") is not None else None,
            "stop_loss_order_reject_transaction": StopLossOrderRejectTransaction.from_dict(obj.get("stopLossOrderRejectTransaction")) if obj.get("stopLossOrderRejectTransaction") is not None else None,
            "trailing_stop_loss_order_cancel_reject_transaction": OrderCancelRejectTransaction.from_dict(obj.get("trailingStopLossOrderCancelRejectTransaction")) if obj.get("trailingStopLossOrderCancelRejectTransaction") is not None else None,
            "trailing_stop_loss_order_reject_transaction": TrailingStopLossOrderRejectTransaction.from_dict(obj.get("trailingStopLossOrderRejectTransaction")) if obj.get("trailingStopLossOrderRejectTransaction") is not None else None,
            "last_transaction_id": obj.get("lastTransactionID"),
            "related_transaction_ids": obj.get("relatedTransactionIDs"),
            "error_code": obj.get("errorCode"),
            "error_message": obj.get("errorMessage")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj


