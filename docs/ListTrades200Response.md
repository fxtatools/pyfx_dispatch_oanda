# ListTrades200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**trades** | [**List[Trade]**](Trade.md) | The list of Trade detail objects | [optional] 
**last_transaction_id** | **str** | The ID of the most recent Transaction created for the Account | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.list_trades200_response import ListTrades200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ListTrades200Response from a JSON string
list_trades200_response_instance = ListTrades200Response.from_json(json)
# print the JSON string representation of the object
print ListTrades200Response.to_json()

# convert the object into a dict
list_trades200_response_dict = list_trades200_response_instance.to_dict()
# create an instance of ListTrades200Response from a dict
list_trades200_response_form_dict = list_trades200_response.from_dict(list_trades200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


