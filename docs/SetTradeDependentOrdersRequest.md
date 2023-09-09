# SetTradeDependentOrdersRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**take_profit** | [**TakeProfitDetails**](TakeProfitDetails.md) |  | [optional] 
**stop_loss** | [**StopLossDetails**](StopLossDetails.md) |  | [optional] 
**trailing_stop_loss** | [**TrailingStopLossDetails**](TrailingStopLossDetails.md) |  | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.set_trade_dependent_orders_request import SetTradeDependentOrdersRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SetTradeDependentOrdersRequest from a JSON string
set_trade_dependent_orders_request_instance = SetTradeDependentOrdersRequest.from_json(json)
# print the JSON string representation of the object
print SetTradeDependentOrdersRequest.to_json()

# convert the object into a dict
set_trade_dependent_orders_request_dict = set_trade_dependent_orders_request_instance.to_dict()
# create an instance of SetTradeDependentOrdersRequest from a dict
set_trade_dependent_orders_request_form_dict = set_trade_dependent_orders_request.from_dict(set_trade_dependent_orders_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


