# SetOrderClientExtensions404Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_client_extensions_modify_reject_transaction** | [**OrderClientExtensionsModifyRejectTransaction**](OrderClientExtensionsModifyRejectTransaction.md) |  | [optional] 
**last_transaction_id** | **str** | The ID of the most recent Transaction created for the Account. Only present if the Account exists. | [optional] 
**related_transaction_ids** | **List[str]** | The IDs of all Transactions that were created while satisfying the request. Only present if the Account exists. | [optional] 
**error_code** | **str** | The code of the error that has occurred. This field may not be returned for some errors. | [optional] 
**error_message** | **str** | The human-readable description of the error that has occurred. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.set_order_client_extensions404_response import SetOrderClientExtensions404Response

# TODO update the JSON string below
json = "{}"
# create an instance of SetOrderClientExtensions404Response from a JSON string
set_order_client_extensions404_response_instance = SetOrderClientExtensions404Response.from_json(json)
# print the JSON string representation of the object
print SetOrderClientExtensions404Response.to_json()

# convert the object into a dict
set_order_client_extensions404_response_dict = set_order_client_extensions404_response_instance.to_dict()
# create an instance of SetOrderClientExtensions404Response from a dict
set_order_client_extensions404_response_form_dict = set_order_client_extensions404_response.from_dict(set_order_client_extensions404_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


