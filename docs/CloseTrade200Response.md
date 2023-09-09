# CloseTrade200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_create_transaction** | [**MarketOrderTransaction**](MarketOrderTransaction.md) |  | [optional] 
**order_fill_transaction** | [**OrderFillTransaction**](OrderFillTransaction.md) |  | [optional] 
**order_cancel_transaction** | [**OrderCancelTransaction**](OrderCancelTransaction.md) |  | [optional] 
**related_transaction_ids** | **List[str]** | The IDs of all Transactions that were created while satisfying the request. | [optional] 
**last_transaction_id** | **str** | The ID of the most recent Transaction created for the Account | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.close_trade200_response import CloseTrade200Response

# TODO update the JSON string below
json = "{}"
# create an instance of CloseTrade200Response from a JSON string
close_trade200_response_instance = CloseTrade200Response.from_json(json)
# print the JSON string representation of the object
print CloseTrade200Response.to_json()

# convert the object into a dict
close_trade200_response_dict = close_trade200_response_instance.to_dict()
# create an instance of CloseTrade200Response from a dict
close_trade200_response_form_dict = close_trade200_response.from_dict(close_trade200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


