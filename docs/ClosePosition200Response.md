# ClosePosition200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**long_order_create_transaction** | [**MarketOrderTransaction**](MarketOrderTransaction.md) |  | [optional] 
**long_order_fill_transaction** | [**OrderFillTransaction**](OrderFillTransaction.md) |  | [optional] 
**long_order_cancel_transaction** | [**OrderCancelTransaction**](OrderCancelTransaction.md) |  | [optional] 
**short_order_create_transaction** | [**MarketOrderTransaction**](MarketOrderTransaction.md) |  | [optional] 
**short_order_fill_transaction** | [**OrderFillTransaction**](OrderFillTransaction.md) |  | [optional] 
**short_order_cancel_transaction** | [**OrderCancelTransaction**](OrderCancelTransaction.md) |  | [optional] 
**related_transaction_ids** | **List[str]** | The IDs of all Transactions that were created while satisfying the request. | [optional] 
**last_transaction_id** | **str** | The ID of the most recent Transaction created for the Account | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.close_position200_response import ClosePosition200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ClosePosition200Response from a JSON string
close_position200_response_instance = ClosePosition200Response.from_json(json)
# print the JSON string representation of the object
print ClosePosition200Response.to_json()

# convert the object into a dict
close_position200_response_dict = close_position200_response_instance.to_dict()
# create an instance of ClosePosition200Response from a dict
close_position200_response_form_dict = close_position200_response.from_dict(close_position200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


