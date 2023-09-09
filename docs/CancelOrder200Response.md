# CancelOrder200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_cancel_transaction** | [**OrderCancelTransaction**](OrderCancelTransaction.md) |  | [optional] 
**related_transaction_ids** | **List[str]** | The IDs of all Transactions that were created while satisfying the request. | [optional] 
**last_transaction_id** | **str** | The ID of the most recent Transaction created for the Account | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.cancel_order200_response import CancelOrder200Response

# TODO update the JSON string below
json = "{}"
# create an instance of CancelOrder200Response from a JSON string
cancel_order200_response_instance = CancelOrder200Response.from_json(json)
# print the JSON string representation of the object
print CancelOrder200Response.to_json()

# convert the object into a dict
cancel_order200_response_dict = cancel_order200_response_instance.to_dict()
# create an instance of CancelOrder200Response from a dict
cancel_order200_response_form_dict = cancel_order200_response.from_dict(cancel_order200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


