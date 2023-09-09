# GetInstrumentCandles400Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error_code** | **str** | The code of the error that has occurred. This field may not be returned for some errors. | [optional] 
**error_message** | **str** | The human-readable description of the error that has occurred. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.get_instrument_candles400_response import GetInstrumentCandles400Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetInstrumentCandles400Response from a JSON string
get_instrument_candles400_response_instance = GetInstrumentCandles400Response.from_json(json)
# print the JSON string representation of the object
print GetInstrumentCandles400Response.to_json()

# convert the object into a dict
get_instrument_candles400_response_dict = get_instrument_candles400_response_instance.to_dict()
# create an instance of GetInstrumentCandles400Response from a dict
get_instrument_candles400_response_form_dict = get_instrument_candles400_response.from_dict(get_instrument_candles400_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


