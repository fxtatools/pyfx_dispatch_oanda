# CalculatedTradeState

The dynamic (calculated) state of an open Trade

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The Trade&#39;s ID. | [optional] 
**unrealized_pl** | **str** | The Trade&#39;s unrealized profit/loss. | [optional] 
**margin_used** | **str** | Margin currently used by the Trade. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.calculated_trade_state import CalculatedTradeState

# TODO update the JSON string below
json = "{}"
# create an instance of CalculatedTradeState from a JSON string
calculated_trade_state_instance = CalculatedTradeState.from_json(json)
# print the JSON string representation of the object
print CalculatedTradeState.to_json()

# convert the object into a dict
calculated_trade_state_dict = calculated_trade_state_instance.to_dict()
# create an instance of CalculatedTradeState from a dict
calculated_trade_state_form_dict = calculated_trade_state.from_dict(calculated_trade_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


