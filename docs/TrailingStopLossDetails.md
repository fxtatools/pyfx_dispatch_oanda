# TrailingStopLossDetails

TrailingStopLossDetails specifies the details of a Trailing Stop Loss Order to be created on behalf of a client. This may happen when an Order is filled that opens a Trade requiring a Trailing Stop Loss, or when a Trade's dependent Trailing Stop Loss Order is modified directly through the Trade.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**distance** | **str** | The distance (in price units) from the Trade&#39;s fill price that the Trailing Stop Loss Order will be triggered at. | [optional] 
**time_in_force** | **str** | The time in force for the created Trailing Stop Loss Order. This may only be GTC, GTD or GFD. | [optional] 
**gtd_time** | **str** | The date when the Trailing Stop Loss Order will be cancelled on if timeInForce is GTD. | [optional] 
**client_extensions** | [**ClientExtensions**](ClientExtensions.md) |  | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.trailing_stop_loss_details import TrailingStopLossDetails

# TODO update the JSON string below
json = "{}"
# create an instance of TrailingStopLossDetails from a JSON string
trailing_stop_loss_details_instance = TrailingStopLossDetails.from_json(json)
# print the JSON string representation of the object
print TrailingStopLossDetails.to_json()

# convert the object into a dict
trailing_stop_loss_details_dict = trailing_stop_loss_details_instance.to_dict()
# create an instance of TrailingStopLossDetails from a dict
trailing_stop_loss_details_form_dict = trailing_stop_loss_details.from_dict(trailing_stop_loss_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


