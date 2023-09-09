# MarketOrder

A MarketOrder is an order that is filled immediately upon creation using the current market price.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The Order&#39;s identifier, unique within the Order&#39;s Account. | [optional] 
**create_time** | **str** | The time when the Order was created. | [optional] 
**state** | **str** | The current state of the Order. | [optional] 
**client_extensions** | [**ClientExtensions**](ClientExtensions.md) |  | [optional] 
**type** | **str** | The type of the Order. Always set to \&quot;MARKET\&quot; for Market Orders. | [optional] 
**instrument** | **str** | The Market Order&#39;s Instrument. | [optional] 
**units** | **str** | The quantity requested to be filled by the Market Order. A posititive number of units results in a long Order, and a negative number of units results in a short Order. | [optional] 
**time_in_force** | **str** | The time-in-force requested for the Market Order. Restricted to FOK or IOC for a MarketOrder. | [optional] 
**price_bound** | **str** | The worst price that the client is willing to have the Market Order filled at. | [optional] 
**position_fill** | **str** | Specification of how Positions in the Account are modified when the Order is filled. | [optional] 
**trade_close** | [**MarketOrderTradeClose**](MarketOrderTradeClose.md) |  | [optional] 
**long_position_closeout** | [**MarketOrderPositionCloseout**](MarketOrderPositionCloseout.md) |  | [optional] 
**short_position_closeout** | [**MarketOrderPositionCloseout**](MarketOrderPositionCloseout.md) |  | [optional] 
**margin_closeout** | [**MarketOrderMarginCloseout**](MarketOrderMarginCloseout.md) |  | [optional] 
**delayed_trade_close** | [**MarketOrderDelayedTradeClose**](MarketOrderDelayedTradeClose.md) |  | [optional] 
**take_profit_on_fill** | [**TakeProfitDetails**](TakeProfitDetails.md) |  | [optional] 
**stop_loss_on_fill** | [**StopLossDetails**](StopLossDetails.md) |  | [optional] 
**trailing_stop_loss_on_fill** | [**TrailingStopLossDetails**](TrailingStopLossDetails.md) |  | [optional] 
**trade_client_extensions** | [**ClientExtensions**](ClientExtensions.md) |  | [optional] 
**filling_transaction_id** | **str** | ID of the Transaction that filled this Order (only provided when the Order&#39;s state is FILLED) | [optional] 
**filled_time** | **str** | Date/time when the Order was filled (only provided when the Order&#39;s state is FILLED) | [optional] 
**trade_opened_id** | **str** | Trade ID of Trade opened when the Order was filled (only provided when the Order&#39;s state is FILLED and a Trade was opened as a result of the fill) | [optional] 
**trade_reduced_id** | **str** | Trade ID of Trade reduced when the Order was filled (only provided when the Order&#39;s state is FILLED and a Trade was reduced as a result of the fill) | [optional] 
**trade_closed_ids** | **List[str]** | Trade IDs of Trades closed when the Order was filled (only provided when the Order&#39;s state is FILLED and one or more Trades were closed as a result of the fill) | [optional] 
**cancelling_transaction_id** | **str** | ID of the Transaction that cancelled the Order (only provided when the Order&#39;s state is CANCELLED) | [optional] 
**cancelled_time** | **str** | Date/time when the Order was cancelled (only provided when the state of the Order is CANCELLED) | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.market_order import MarketOrder

# TODO update the JSON string below
json = "{}"
# create an instance of MarketOrder from a JSON string
market_order_instance = MarketOrder.from_json(json)
# print the JSON string representation of the object
print MarketOrder.to_json()

# convert the object into a dict
market_order_dict = market_order_instance.to_dict()
# create an instance of MarketOrder from a dict
market_order_form_dict = market_order.from_dict(market_order_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


