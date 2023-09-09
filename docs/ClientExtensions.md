# ClientExtensions

A ClientExtensions object allows a client to attach a clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if your account is associated with MT4.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The Client ID of the Order/Trade | [optional] 
**tag** | **str** | A tag associated with the Order/Trade | [optional] 
**comment** | **str** | A comment associated with the Order/Trade | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.client_extensions import ClientExtensions

# TODO update the JSON string below
json = "{}"
# create an instance of ClientExtensions from a JSON string
client_extensions_instance = ClientExtensions.from_json(json)
# print the JSON string representation of the object
print ClientExtensions.to_json()

# convert the object into a dict
client_extensions_dict = client_extensions_instance.to_dict()
# create an instance of ClientExtensions from a dict
client_extensions_form_dict = client_extensions.from_dict(client_extensions_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


