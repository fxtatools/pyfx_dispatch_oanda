# ConfigureAccountRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**alias** | **str** | Client-defined alias (name) for the Account | [optional] 
**margin_rate** | **str** | The string representation of a decimal number. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.configure_account_request import ConfigureAccountRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ConfigureAccountRequest from a JSON string
configure_account_request_instance = ConfigureAccountRequest.from_json(json)
# print the JSON string representation of the object
print ConfigureAccountRequest.to_json()

# convert the object into a dict
configure_account_request_dict = configure_account_request_instance.to_dict()
# create an instance of ConfigureAccountRequest from a dict
configure_account_request_form_dict = configure_account_request.from_dict(configure_account_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


