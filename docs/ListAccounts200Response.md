# ListAccounts200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**accounts** | [**List[AccountProperties]**](AccountProperties.md) | The list of Accounts the client is authorized to access and their associated properties. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.list_accounts200_response import ListAccounts200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ListAccounts200Response from a JSON string
list_accounts200_response_instance = ListAccounts200Response.from_json(json)
# print the JSON string representation of the object
print ListAccounts200Response.to_json()

# convert the object into a dict
list_accounts200_response_dict = list_accounts200_response_instance.to_dict()
# create an instance of ListAccounts200Response from a dict
list_accounts200_response_form_dict = list_accounts200_response.from_dict(list_accounts200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


