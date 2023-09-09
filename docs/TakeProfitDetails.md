# TakeProfitDetails

TakeProfitDetails specifies the details of a Take Profit Order to be created on behalf of a client. This may happen when an Order is filled that opens a Trade requiring a Take Profit, or when a Trade's dependent Take Profit Order is modified directly through the Trade.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**price** | **str** | The price that the Take Profit Order will be triggered at. Only one of the price and distance fields may be specified. | [optional] 
**time_in_force** | **str** | The time in force for the created Take Profit Order. This may only be GTC, GTD or GFD. | [optional] 
**gtd_time** | **str** | The date when the Take Profit Order will be cancelled on if timeInForce is GTD. | [optional] 
**client_extensions** | [**ClientExtensions**](ClientExtensions.md) |  | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.take_profit_details import TakeProfitDetails

# TODO update the JSON string below
json = "{}"
# create an instance of TakeProfitDetails from a JSON string
take_profit_details_instance = TakeProfitDetails.from_json(json)
# print the JSON string representation of the object
print TakeProfitDetails.to_json()

# convert the object into a dict
take_profit_details_dict = take_profit_details_instance.to_dict()
# create an instance of TakeProfitDetails from a dict
take_profit_details_form_dict = take_profit_details.from_dict(take_profit_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


