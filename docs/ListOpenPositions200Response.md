# ListOpenPositions200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**positions** | [**List[Position]**](Position.md) | The list of open Positions in the Account. | [optional] 
**last_transaction_id** | **str** | The ID of the most recent Transaction created for the Account | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.list_open_positions200_response import ListOpenPositions200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ListOpenPositions200Response from a JSON string
list_open_positions200_response_instance = ListOpenPositions200Response.from_json(json)
# print the JSON string representation of the object
print ListOpenPositions200Response.to_json()

# convert the object into a dict
list_open_positions200_response_dict = list_open_positions200_response_instance.to_dict()
# create an instance of ListOpenPositions200Response from a dict
list_open_positions200_response_form_dict = list_open_positions200_response.from_dict(list_open_positions200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


