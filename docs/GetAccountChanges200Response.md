# GetAccountChanges200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**changes** | [**AccountChanges**](AccountChanges.md) |  | [optional] 
**state** | [**AccountChangesState**](AccountChangesState.md) |  | [optional] 
**last_transaction_id** | **str** | The ID of the last Transaction created for the Account.  This Transaction ID should be used for future poll requests, as the client has already observed all changes up to and including it. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.get_account_changes200_response import GetAccountChanges200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetAccountChanges200Response from a JSON string
get_account_changes200_response_instance = GetAccountChanges200Response.from_json(json)
# print the JSON string representation of the object
print GetAccountChanges200Response.to_json()

# convert the object into a dict
get_account_changes200_response_dict = get_account_changes200_response_instance.to_dict()
# create an instance of GetAccountChanges200Response from a dict
get_account_changes200_response_form_dict = get_account_changes200_response.from_dict(get_account_changes200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


