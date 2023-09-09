# GetInstrumentPrice200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**price** | [**Price**](Price.md) |  | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.get_instrument_price200_response import GetInstrumentPrice200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetInstrumentPrice200Response from a JSON string
get_instrument_price200_response_instance = GetInstrumentPrice200Response.from_json(json)
# print the JSON string representation of the object
print GetInstrumentPrice200Response.to_json()

# convert the object into a dict
get_instrument_price200_response_dict = get_instrument_price200_response_instance.to_dict()
# create an instance of GetInstrumentPrice200Response from a dict
get_instrument_price200_response_form_dict = get_instrument_price200_response.from_dict(get_instrument_price200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


