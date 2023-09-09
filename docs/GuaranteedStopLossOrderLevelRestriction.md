# GuaranteedStopLossOrderLevelRestriction

A GuaranteedStopLossOrderLevelRestriction represents the total position size that can exist within a given price window for Trades with guaranteed Stop Loss Orders attached for a specific Instrument.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**volume** | **str** | Applies to Trades with a guaranteed Stop Loss Order attached for the specified Instrument. This is the total allowed Trade volume that can exist within the priceRange based on the trigger prices of the guaranteed Stop Loss Orders. | [optional] 
**price_range** | **str** | The price range the volume applies to. This value is in price units. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.guaranteed_stop_loss_order_level_restriction import GuaranteedStopLossOrderLevelRestriction

# TODO update the JSON string below
json = "{}"
# create an instance of GuaranteedStopLossOrderLevelRestriction from a JSON string
guaranteed_stop_loss_order_level_restriction_instance = GuaranteedStopLossOrderLevelRestriction.from_json(json)
# print the JSON string representation of the object
print GuaranteedStopLossOrderLevelRestriction.to_json()

# convert the object into a dict
guaranteed_stop_loss_order_level_restriction_dict = guaranteed_stop_loss_order_level_restriction_instance.to_dict()
# create an instance of GuaranteedStopLossOrderLevelRestriction from a dict
guaranteed_stop_loss_order_level_restriction_form_dict = guaranteed_stop_loss_order_level_restriction.from_dict(guaranteed_stop_loss_order_level_restriction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


