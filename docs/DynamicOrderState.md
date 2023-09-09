# DynamicOrderState

The dynamic state of an Order. This is only relevant to TrailingStopLoss Orders, as no other Order type has dynamic state.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The Order&#39;s ID. | [optional] 
**trailing_stop_value** | **str** | The Order&#39;s calculated trailing stop value. | [optional] 
**trigger_distance** | **str** | The distance between the Trailing Stop Loss Order&#39;s trailingStopValue and the current Market Price. This represents the distance (in price units) of the Order from a triggering price. If the distance could not be determined, this value will not be set. | [optional] 
**is_trigger_distance_exact** | **bool** | True if an exact trigger distance could be calculated. If false, it means the provided trigger distance is a best estimate. If the distance could not be determined, this value will not be set. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.dynamic_order_state import DynamicOrderState

# TODO update the JSON string below
json = "{}"
# create an instance of DynamicOrderState from a JSON string
dynamic_order_state_instance = DynamicOrderState.from_json(json)
# print the JSON string representation of the object
print DynamicOrderState.to_json()

# convert the object into a dict
dynamic_order_state_dict = dynamic_order_state_instance.to_dict()
# create an instance of DynamicOrderState from a dict
dynamic_order_state_form_dict = dynamic_order_state.from_dict(dynamic_order_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


