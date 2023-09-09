# LiquidityRegenerationSchedule

A LiquidityRegenerationSchedule indicates how liquidity that is used when filling an Order for an instrument is regenerated following the fill.  A liquidity regeneration schedule will be in effect until the timestamp of its final step, but may be replaced by a schedule created for an Order of the same instrument that is filled while it is still in effect.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**steps** | [**List[LiquidityRegenerationScheduleStep]**](LiquidityRegenerationScheduleStep.md) | The steps in the Liquidity Regeneration Schedule | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.liquidity_regeneration_schedule import LiquidityRegenerationSchedule

# TODO update the JSON string below
json = "{}"
# create an instance of LiquidityRegenerationSchedule from a JSON string
liquidity_regeneration_schedule_instance = LiquidityRegenerationSchedule.from_json(json)
# print the JSON string representation of the object
print LiquidityRegenerationSchedule.to_json()

# convert the object into a dict
liquidity_regeneration_schedule_dict = liquidity_regeneration_schedule_instance.to_dict()
# create an instance of LiquidityRegenerationSchedule from a dict
liquidity_regeneration_schedule_form_dict = liquidity_regeneration_schedule.from_dict(liquidity_regeneration_schedule_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


