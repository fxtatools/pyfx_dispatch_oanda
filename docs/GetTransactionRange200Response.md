# GetTransactionRange200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transactions** | [**List[Transaction]**](Transaction.md) | The list of Transactions that satisfy the request. | [optional] 
**last_transaction_id** | **str** | The ID of the most recent Transaction created for the Account | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.get_transaction_range200_response import GetTransactionRange200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetTransactionRange200Response from a JSON string
get_transaction_range200_response_instance = GetTransactionRange200Response.from_json(json)
# print the JSON string representation of the object
print GetTransactionRange200Response.to_json()

# convert the object into a dict
get_transaction_range200_response_dict = get_transaction_range200_response_instance.to_dict()
# create an instance of GetTransactionRange200Response from a dict
get_transaction_range200_response_form_dict = get_transaction_range200_response.from_dict(get_transaction_range200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


