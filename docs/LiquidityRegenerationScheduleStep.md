# LiquidityRegenerationScheduleStep

A liquidity regeneration schedule Step indicates the amount of bid and ask liquidity that is used by the Account at a certain time. These amounts will only change at the timestamp of the following step.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**timestamp** | **str** | The timestamp of the schedule step. | [optional] 
**bid_liquidity_used** | **str** | The amount of bid liquidity used at this step in the schedule. | [optional] 
**ask_liquidity_used** | **str** | The amount of ask liquidity used at this step in the schedule. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.liquidity_regeneration_schedule_step import LiquidityRegenerationScheduleStep

# TODO update the JSON string below
json = "{}"
# create an instance of LiquidityRegenerationScheduleStep from a JSON string
liquidity_regeneration_schedule_step_instance = LiquidityRegenerationScheduleStep.from_json(json)
# print the JSON string representation of the object
print LiquidityRegenerationScheduleStep.to_json()

# convert the object into a dict
liquidity_regeneration_schedule_step_dict = liquidity_regeneration_schedule_step_instance.to_dict()
# create an instance of LiquidityRegenerationScheduleStep from a dict
liquidity_regeneration_schedule_step_form_dict = liquidity_regeneration_schedule_step.from_dict(liquidity_regeneration_schedule_step_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


