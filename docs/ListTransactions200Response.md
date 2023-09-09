# ListTransactions200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_from** | **str** | The starting time provided in the request. | [optional] 
**to** | **str** | The ending time provided in the request. | [optional] 
**page_size** | **int** | The pageSize provided in the request | [optional] 
**type** | **List[str]** | The Transaction-type filter provided in the request | [optional] 
**count** | **int** | The number of Transactions that are contained in the pages returned | [optional] 
**pages** | **List[str]** | The list of URLs that represent idrange queries providing the data for each page in the query results | [optional] 
**last_transaction_id** | **str** | The ID of the most recent Transaction created for the Account | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.list_transactions200_response import ListTransactions200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ListTransactions200Response from a JSON string
list_transactions200_response_instance = ListTransactions200Response.from_json(json)
# print the JSON string representation of the object
print ListTransactions200Response.to_json()

# convert the object into a dict
list_transactions200_response_dict = list_transactions200_response_instance.to_dict()
# create an instance of ListTransactions200Response from a dict
list_transactions200_response_form_dict = list_transactions200_response.from_dict(list_transactions200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


