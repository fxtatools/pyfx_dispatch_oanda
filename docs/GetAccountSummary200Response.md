# GetAccountSummary200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**account** | [**AccountSummary**](AccountSummary.md) |  | [optional] 
**last_transaction_id** | **str** | The ID of the most recent Transaction created for the Account. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.get_account_summary200_response import GetAccountSummary200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetAccountSummary200Response from a JSON string
get_account_summary200_response_instance = GetAccountSummary200Response.from_json(json)
# print the JSON string representation of the object
print GetAccountSummary200Response.to_json()

# convert the object into a dict
get_account_summary200_response_dict = get_account_summary200_response_instance.to_dict()
# create an instance of GetAccountSummary200Response from a dict
get_account_summary200_response_form_dict = get_account_summary200_response.from_dict(get_account_summary200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


