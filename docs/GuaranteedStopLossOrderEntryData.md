# GuaranteedStopLossOrderEntryData

Details required by clients creating a Guaranteed Stop Loss Order

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**minimum_distance** | **str** | The minimum distance allowed between the Trade&#39;s fill price and the configured price for guaranteed Stop Loss Orders created for this instrument. Specified in price units. | [optional] 
**premium** | **str** | The amount that is charged to the account if a guaranteed Stop Loss Order is triggered and filled. The value is in price units and is charged for each unit of the Trade. | [optional] 
**level_restriction** | [**GuaranteedStopLossOrderLevelRestriction**](GuaranteedStopLossOrderLevelRestriction.md) |  | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.guaranteed_stop_loss_order_entry_data import GuaranteedStopLossOrderEntryData

# TODO update the JSON string below
json = "{}"
# create an instance of GuaranteedStopLossOrderEntryData from a JSON string
guaranteed_stop_loss_order_entry_data_instance = GuaranteedStopLossOrderEntryData.from_json(json)
# print the JSON string representation of the object
print GuaranteedStopLossOrderEntryData.to_json()

# convert the object into a dict
guaranteed_stop_loss_order_entry_data_dict = guaranteed_stop_loss_order_entry_data_instance.to_dict()
# create an instance of GuaranteedStopLossOrderEntryData from a dict
guaranteed_stop_loss_order_entry_data_form_dict = guaranteed_stop_loss_order_entry_data.from_dict(guaranteed_stop_loss_order_entry_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


