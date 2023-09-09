# SetOrderClientExtensions200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_client_extensions_modify_transaction** | [**OrderClientExtensionsModifyTransaction**](OrderClientExtensionsModifyTransaction.md) |  | [optional] 
**last_transaction_id** | **str** | The ID of the most recent Transaction created for the Account | [optional] 
**related_transaction_ids** | **List[str]** | The IDs of all Transactions that were created while satisfying the request. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.set_order_client_extensions200_response import SetOrderClientExtensions200Response

# TODO update the JSON string below
json = "{}"
# create an instance of SetOrderClientExtensions200Response from a JSON string
set_order_client_extensions200_response_instance = SetOrderClientExtensions200Response.from_json(json)
# print the JSON string representation of the object
print SetOrderClientExtensions200Response.to_json()

# convert the object into a dict
set_order_client_extensions200_response_dict = set_order_client_extensions200_response_instance.to_dict()
# create an instance of SetOrderClientExtensions200Response from a dict
set_order_client_extensions200_response_form_dict = set_order_client_extensions200_response.from_dict(set_order_client_extensions200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


