# StopLossDetails

StopLossDetails specifies the details of a Stop Loss Order to be created on behalf of a client. This may happen when an Order is filled that opens a Trade requiring a Stop Loss, or when a Trade's dependent Stop Loss Order is modified directly through the Trade.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**price** | **str** | The price that the Stop Loss Order will be triggered at. Only one of the price and distance fields may be specified. | [optional] 
**distance** | **str** | Specifies the distance (in price units) from the Trade&#39;s open price to use as the Stop Loss Order price. Only one of the distance and price fields may be specified. | [optional] 
**time_in_force** | **str** | The time in force for the created Stop Loss Order. This may only be GTC, GTD or GFD. | [optional] 
**gtd_time** | **str** | The date when the Stop Loss Order will be cancelled on if timeInForce is GTD. | [optional] 
**client_extensions** | [**ClientExtensions**](ClientExtensions.md) |  | [optional] 
**guaranteed** | **bool** | Flag indicating that the price for the Stop Loss Order is guaranteed. The default value depends on the GuaranteedStopLossOrderMode of the account, if it is REQUIRED, the default will be true, for DISABLED or ENABLED the default is false. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.stop_loss_details import StopLossDetails

# TODO update the JSON string below
json = "{}"
# create an instance of StopLossDetails from a JSON string
stop_loss_details_instance = StopLossDetails.from_json(json)
# print the JSON string representation of the object
print StopLossDetails.to_json()

# convert the object into a dict
stop_loss_details_dict = stop_loss_details_instance.to_dict()
# create an instance of StopLossDetails from a dict
stop_loss_details_form_dict = stop_loss_details.from_dict(stop_loss_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


