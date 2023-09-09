# MarketOrderTradeClose

A MarketOrderTradeClose specifies the extensions to a Market Order that has been created specifically to close a Trade.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**trade_id** | **str** | The ID of the Trade requested to be closed | [optional] 
**client_trade_id** | **str** | The client ID of the Trade requested to be closed | [optional] 
**units** | **str** | Indication of how much of the Trade to close. Either \&quot;ALL\&quot;, or a DecimalNumber reflection a partial close of the Trade. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.market_order_trade_close import MarketOrderTradeClose

# TODO update the JSON string below
json = "{}"
# create an instance of MarketOrderTradeClose from a JSON string
market_order_trade_close_instance = MarketOrderTradeClose.from_json(json)
# print the JSON string representation of the object
print MarketOrderTradeClose.to_json()

# convert the object into a dict
market_order_trade_close_dict = market_order_trade_close_instance.to_dict()
# create an instance of MarketOrderTradeClose from a dict
market_order_trade_close_form_dict = market_order_trade_close.from_dict(market_order_trade_close_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


