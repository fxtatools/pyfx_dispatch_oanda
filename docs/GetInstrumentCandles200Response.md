# GetInstrumentCandles200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**instrument** | **str** | The instrument whose Prices are represented by the candlesticks. | [optional] 
**granularity** | **str** | The granularity of the candlesticks provided. | [optional] 
**candles** | [**List[Candlestick]**](Candlestick.md) | The list of candlesticks that satisfy the request. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.get_instrument_candles200_response import GetInstrumentCandles200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetInstrumentCandles200Response from a JSON string
get_instrument_candles200_response_instance = GetInstrumentCandles200Response.from_json(json)
# print the JSON string representation of the object
print GetInstrumentCandles200Response.to_json()

# convert the object into a dict
get_instrument_candles200_response_dict = get_instrument_candles200_response_instance.to_dict()
# create an instance of GetInstrumentCandles200Response from a dict
get_instrument_candles200_response_form_dict = get_instrument_candles200_response.from_dict(get_instrument_candles200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


