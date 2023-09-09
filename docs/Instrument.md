# Instrument

Full specification of an Instrument.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the Instrument | [optional] 
**type** | **str** | The type of the Instrument | [optional] 
**display_name** | **str** | The display name of the Instrument | [optional] 
**pip_location** | **int** | The location of the \&quot;pip\&quot; for this instrument. The decimal position of the pip in this Instrument&#39;s price can be found at 10 ^ pipLocation (e.g. -4 pipLocation results in a decimal pip position of 10 ^ -4 &#x3D; 0.0001). | [optional] 
**display_precision** | **int** | The number of decimal places that should be used to display prices for this instrument. (e.g. a displayPrecision of 5 would result in a price of \&quot;1\&quot; being displayed as \&quot;1.00000\&quot;) | [optional] 
**trade_units_precision** | **int** | The amount of decimal places that may be provided when specifying the number of units traded for this instrument. | [optional] 
**minimum_trade_size** | **str** | The smallest number of units allowed to be traded for this instrument. | [optional] 
**maximum_trailing_stop_distance** | **str** | The maximum trailing stop distance allowed for a trailing stop loss created for this instrument. Specified in price units. | [optional] 
**minimum_trailing_stop_distance** | **str** | The minimum trailing stop distance allowed for a trailing stop loss created for this instrument. Specified in price units. | [optional] 
**maximum_position_size** | **str** | The maximum position size allowed for this instrument. Specified in units. | [optional] 
**maximum_order_units** | **str** | The maximum units allowed for an Order placed for this instrument. Specified in units. | [optional] 
**margin_rate** | **str** | The margin rate for this instrument. | [optional] 
**commission** | [**InstrumentCommission**](InstrumentCommission.md) |  | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.instrument import Instrument

# TODO update the JSON string below
json = "{}"
# create an instance of Instrument from a JSON string
instrument_instance = Instrument.from_json(json)
# print the JSON string representation of the object
print Instrument.to_json()

# convert the object into a dict
instrument_dict = instrument_instance.to_dict()
# create an instance of Instrument from a dict
instrument_form_dict = instrument.from_dict(instrument_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


