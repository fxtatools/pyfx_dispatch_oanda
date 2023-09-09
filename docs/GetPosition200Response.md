# GetPosition200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**position** | [**Position**](Position.md) |  | [optional] 
**last_transaction_id** | **str** | The ID of the most recent Transaction created for the Account | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.get_position200_response import GetPosition200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetPosition200Response from a JSON string
get_position200_response_instance = GetPosition200Response.from_json(json)
# print the JSON string representation of the object
print GetPosition200Response.to_json()

# convert the object into a dict
get_position200_response_dict = get_position200_response_instance.to_dict()
# create an instance of GetPosition200Response from a dict
get_position200_response_form_dict = get_position200_response.from_dict(get_position200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


