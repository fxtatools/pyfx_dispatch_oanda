# MarketOrderPositionCloseout

A MarketOrderPositionCloseout specifies the extensions to a Market Order when it has been created to closeout a specific Position.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**instrument** | **str** | The instrument of the Position being closed out. | [optional] 
**units** | **str** | Indication of how much of the Position to close. Either \&quot;ALL\&quot;, or a DecimalNumber reflection a partial close of the Trade. The DecimalNumber must always be positive, and represent a number that doesn&#39;t exceed the absolute size of the Position. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.market_order_position_closeout import MarketOrderPositionCloseout

# TODO update the JSON string below
json = "{}"
# create an instance of MarketOrderPositionCloseout from a JSON string
market_order_position_closeout_instance = MarketOrderPositionCloseout.from_json(json)
# print the JSON string representation of the object
print MarketOrderPositionCloseout.to_json()

# convert the object into a dict
market_order_position_closeout_dict = market_order_position_closeout_instance.to_dict()
# create an instance of MarketOrderPositionCloseout from a dict
market_order_position_closeout_form_dict = market_order_position_closeout.from_dict(market_order_position_closeout_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


