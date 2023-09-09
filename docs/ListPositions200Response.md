# ListPositions200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**positions** | [**List[Position]**](Position.md) | The list of Account Positions. | [optional] 
**last_transaction_id** | **str** | The ID of the most recent Transaction created for the Account | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.list_positions200_response import ListPositions200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ListPositions200Response from a JSON string
list_positions200_response_instance = ListPositions200Response.from_json(json)
# print the JSON string representation of the object
print ListPositions200Response.to_json()

# convert the object into a dict
list_positions200_response_dict = list_positions200_response_instance.to_dict()
# create an instance of ListPositions200Response from a dict
list_positions200_response_form_dict = list_positions200_response.from_dict(list_positions200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


