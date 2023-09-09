# SetOrderClientExtensionsRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**client_extensions** | [**ClientExtensions**](ClientExtensions.md) |  | [optional] 
**trade_client_extensions** | [**ClientExtensions**](ClientExtensions.md) |  | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.set_order_client_extensions_request import SetOrderClientExtensionsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SetOrderClientExtensionsRequest from a JSON string
set_order_client_extensions_request_instance = SetOrderClientExtensionsRequest.from_json(json)
# print the JSON string representation of the object
print SetOrderClientExtensionsRequest.to_json()

# convert the object into a dict
set_order_client_extensions_request_dict = set_order_client_extensions_request_instance.to_dict()
# create an instance of SetOrderClientExtensionsRequest from a dict
set_order_client_extensions_request_form_dict = set_order_client_extensions_request.from_dict(set_order_client_extensions_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


