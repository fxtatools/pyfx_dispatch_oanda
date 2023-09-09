# ConfigureAccount200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**client_configure_transaction** | [**ClientConfigureTransaction**](ClientConfigureTransaction.md) |  | [optional] 
**last_transaction_id** | **str** | The ID of the last Transaction created for the Account. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.configure_account200_response import ConfigureAccount200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ConfigureAccount200Response from a JSON string
configure_account200_response_instance = ConfigureAccount200Response.from_json(json)
# print the JSON string representation of the object
print ConfigureAccount200Response.to_json()

# convert the object into a dict
configure_account200_response_dict = configure_account200_response_instance.to_dict()
# create an instance of ConfigureAccount200Response from a dict
configure_account200_response_form_dict = configure_account200_response.from_dict(configure_account200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


