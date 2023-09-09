# MarketOrderMarginCloseout

Details for the Market Order extensions specific to a Market Order placed that is part of a Market Order Margin Closeout in a client's account

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reason** | **str** | The reason the Market Order was created to perform a margin closeout | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.market_order_margin_closeout import MarketOrderMarginCloseout

# TODO update the JSON string below
json = "{}"
# create an instance of MarketOrderMarginCloseout from a JSON string
market_order_margin_closeout_instance = MarketOrderMarginCloseout.from_json(json)
# print the JSON string representation of the object
print MarketOrderMarginCloseout.to_json()

# convert the object into a dict
market_order_margin_closeout_dict = market_order_margin_closeout_instance.to_dict()
# create an instance of MarketOrderMarginCloseout from a dict
market_order_margin_closeout_form_dict = market_order_margin_closeout.from_dict(market_order_margin_closeout_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


