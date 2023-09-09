# CalculatedPositionState

The dynamic (calculated) state of a Position

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**instrument** | **str** | The Position&#39;s Instrument. | [optional] 
**net_unrealized_pl** | **str** | The Position&#39;s net unrealized profit/loss | [optional] 
**long_unrealized_pl** | **str** | The unrealized profit/loss of the Position&#39;s long open Trades | [optional] 
**short_unrealized_pl** | **str** | The unrealized profit/loss of the Position&#39;s short open Trades | [optional] 
**margin_used** | **str** | Margin currently used by the Position. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.calculated_position_state import CalculatedPositionState

# TODO update the JSON string below
json = "{}"
# create an instance of CalculatedPositionState from a JSON string
calculated_position_state_instance = CalculatedPositionState.from_json(json)
# print the JSON string representation of the object
print CalculatedPositionState.to_json()

# convert the object into a dict
calculated_position_state_dict = calculated_position_state_instance.to_dict()
# create an instance of CalculatedPositionState from a dict
calculated_position_state_form_dict = calculated_position_state.from_dict(calculated_position_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


