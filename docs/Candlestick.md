# Candlestick

The Candlestick representation

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**time** | **str** | The start time of the candlestick | [optional] 
**bid** | [**CandlestickData**](CandlestickData.md) |  | [optional] 
**ask** | [**CandlestickData**](CandlestickData.md) |  | [optional] 
**mid** | [**CandlestickData**](CandlestickData.md) |  | [optional] 
**volume** | **int** | The number of prices created during the time-range represented by the candlestick. | [optional] 
**complete** | **bool** | A flag indicating if the candlestick is complete. A complete candlestick is one whose ending time is not in the future. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.candlestick import Candlestick

# TODO update the JSON string below
json = "{}"
# create an instance of Candlestick from a JSON string
candlestick_instance = Candlestick.from_json(json)
# print the JSON string representation of the object
print Candlestick.to_json()

# convert the object into a dict
candlestick_dict = candlestick_instance.to_dict()
# create an instance of Candlestick from a dict
candlestick_form_dict = candlestick.from_dict(candlestick_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


