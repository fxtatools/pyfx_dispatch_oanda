# GetInstrumentPriceRange200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prices** | [**List[Price]**](Price.md) | The list of prices that satisfy the request. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.get_instrument_price_range200_response import GetInstrumentPriceRange200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetInstrumentPriceRange200Response from a JSON string
get_instrument_price_range200_response_instance = GetInstrumentPriceRange200Response.from_json(json)
# print the JSON string representation of the object
print GetInstrumentPriceRange200Response.to_json()

# convert the object into a dict
get_instrument_price_range200_response_dict = get_instrument_price_range200_response_instance.to_dict()
# create an instance of GetInstrumentPriceRange200Response from a dict
get_instrument_price_range200_response_form_dict = get_instrument_price_range200_response.from_dict(get_instrument_price_range200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


