# MarketOrderDelayedTradeClose

Details for the Market Order extensions specific to a Market Order placed with the intent of fully closing a specific open trade that should have already been closed but wasn't due to halted market conditions

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**trade_id** | **str** | The ID of the Trade being closed | [optional] 
**client_trade_id** | **str** | The Client ID of the Trade being closed | [optional] 
**source_transaction_id** | **str** | The Transaction ID of the DelayedTradeClosure transaction to which this Delayed Trade Close belongs to | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.market_order_delayed_trade_close import MarketOrderDelayedTradeClose

# TODO update the JSON string below
json = "{}"
# create an instance of MarketOrderDelayedTradeClose from a JSON string
market_order_delayed_trade_close_instance = MarketOrderDelayedTradeClose.from_json(json)
# print the JSON string representation of the object
print MarketOrderDelayedTradeClose.to_json()

# convert the object into a dict
market_order_delayed_trade_close_dict = market_order_delayed_trade_close_instance.to_dict()
# create an instance of MarketOrderDelayedTradeClose from a dict
market_order_delayed_trade_close_form_dict = market_order_delayed_trade_close.from_dict(market_order_delayed_trade_close_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


