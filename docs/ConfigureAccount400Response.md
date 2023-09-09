# ConfigureAccount400Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**client_configure_reject_transaction** | [**ClientConfigureRejectTransaction**](ClientConfigureRejectTransaction.md) |  | [optional] 
**last_transaction_id** | **str** | The ID of the last Transaction created for the Account. | [optional] 
**error_code** | **str** | The code of the error that has occurred. This field may not be returned for some errors. | [optional] 
**error_message** | **str** | The human-readable description of the error that has occurred. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.configure_account400_response import ConfigureAccount400Response

# TODO update the JSON string below
json = "{}"
# create an instance of ConfigureAccount400Response from a JSON string
configure_account400_response_instance = ConfigureAccount400Response.from_json(json)
# print the JSON string representation of the object
print ConfigureAccount400Response.to_json()

# convert the object into a dict
configure_account400_response_dict = configure_account400_response_instance.to_dict()
# create an instance of ConfigureAccount400Response from a dict
configure_account400_response_form_dict = configure_account400_response.from_dict(configure_account400_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


