# CandlestickData

The price data (open, high, low, close) for the Candlestick representation.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**o** | **str** | The first (open) price in the time-range represented by the candlestick. | [optional] 
**h** | **str** | The highest price in the time-range represented by the candlestick. | [optional] 
**l** | **str** | The lowest price in the time-range represented by the candlestick. | [optional] 
**c** | **str** | The last (closing) price in the time-range represented by the candlestick. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.candlestick_data import CandlestickData

# TODO update the JSON string below
json = "{}"
# create an instance of CandlestickData from a JSON string
candlestick_data_instance = CandlestickData.from_json(json)
# print the JSON string representation of the object
print CandlestickData.to_json()

# convert the object into a dict
candlestick_data_dict = candlestick_data_instance.to_dict()
# create an instance of CandlestickData from a dict
candlestick_data_form_dict = candlestick_data.from_dict(candlestick_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


