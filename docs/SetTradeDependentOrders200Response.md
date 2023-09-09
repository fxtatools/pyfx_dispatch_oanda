# SetTradeDependentOrders200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**take_profit_order_cancel_transaction** | [**OrderCancelTransaction**](OrderCancelTransaction.md) |  | [optional] 
**take_profit_order_transaction** | [**TakeProfitOrderTransaction**](TakeProfitOrderTransaction.md) |  | [optional] 
**take_profit_order_fill_transaction** | [**OrderFillTransaction**](OrderFillTransaction.md) |  | [optional] 
**take_profit_order_created_cancel_transaction** | [**OrderCancelTransaction**](OrderCancelTransaction.md) |  | [optional] 
**stop_loss_order_cancel_transaction** | [**OrderCancelTransaction**](OrderCancelTransaction.md) |  | [optional] 
**stop_loss_order_transaction** | [**StopLossOrderTransaction**](StopLossOrderTransaction.md) |  | [optional] 
**stop_loss_order_fill_transaction** | [**OrderFillTransaction**](OrderFillTransaction.md) |  | [optional] 
**stop_loss_order_created_cancel_transaction** | [**OrderCancelTransaction**](OrderCancelTransaction.md) |  | [optional] 
**trailing_stop_loss_order_cancel_transaction** | [**OrderCancelTransaction**](OrderCancelTransaction.md) |  | [optional] 
**trailing_stop_loss_order_transaction** | [**TrailingStopLossOrderTransaction**](TrailingStopLossOrderTransaction.md) |  | [optional] 
**related_transaction_ids** | **List[str]** | The IDs of all Transactions that were created while satisfying the request. | [optional] 
**last_transaction_id** | **str** | The ID of the most recent Transaction created for the Account | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.set_trade_dependent_orders200_response import SetTradeDependentOrders200Response

# TODO update the JSON string below
json = "{}"
# create an instance of SetTradeDependentOrders200Response from a JSON string
set_trade_dependent_orders200_response_instance = SetTradeDependentOrders200Response.from_json(json)
# print the JSON string representation of the object
print SetTradeDependentOrders200Response.to_json()

# convert the object into a dict
set_trade_dependent_orders200_response_dict = set_trade_dependent_orders200_response_instance.to_dict()
# create an instance of SetTradeDependentOrders200Response from a dict
set_trade_dependent_orders200_response_form_dict = set_trade_dependent_orders200_response.from_dict(set_trade_dependent_orders200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


