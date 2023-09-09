# SetTradeDependentOrders400Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**take_profit_order_cancel_reject_transaction** | [**OrderCancelRejectTransaction**](OrderCancelRejectTransaction.md) |  | [optional] 
**take_profit_order_reject_transaction** | [**TakeProfitOrderRejectTransaction**](TakeProfitOrderRejectTransaction.md) |  | [optional] 
**stop_loss_order_cancel_reject_transaction** | [**OrderCancelRejectTransaction**](OrderCancelRejectTransaction.md) |  | [optional] 
**stop_loss_order_reject_transaction** | [**StopLossOrderRejectTransaction**](StopLossOrderRejectTransaction.md) |  | [optional] 
**trailing_stop_loss_order_cancel_reject_transaction** | [**OrderCancelRejectTransaction**](OrderCancelRejectTransaction.md) |  | [optional] 
**trailing_stop_loss_order_reject_transaction** | [**TrailingStopLossOrderRejectTransaction**](TrailingStopLossOrderRejectTransaction.md) |  | [optional] 
**last_transaction_id** | **str** | The ID of the most recent Transaction created for the Account. | [optional] 
**related_transaction_ids** | **List[str]** | The IDs of all Transactions that were created while satisfying the request. | [optional] 
**error_code** | **str** | The code of the error that has occurred. This field may not be returned for some errors. | [optional] 
**error_message** | **str** | The human-readable description of the error that has occurred. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.set_trade_dependent_orders400_response import SetTradeDependentOrders400Response

# TODO update the JSON string below
json = "{}"
# create an instance of SetTradeDependentOrders400Response from a JSON string
set_trade_dependent_orders400_response_instance = SetTradeDependentOrders400Response.from_json(json)
# print the JSON string representation of the object
print SetTradeDependentOrders400Response.to_json()

# convert the object into a dict
set_trade_dependent_orders400_response_dict = set_trade_dependent_orders400_response_instance.to_dict()
# create an instance of SetTradeDependentOrders400Response from a dict
set_trade_dependent_orders400_response_form_dict = set_trade_dependent_orders400_response.from_dict(set_trade_dependent_orders400_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


