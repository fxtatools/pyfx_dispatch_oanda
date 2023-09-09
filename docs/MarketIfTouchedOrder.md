# MarketIfTouchedOrder

A MarketIfTouchedOrder is an order that is created with a price threshold, and will only be filled by a market price that is touches or crosses the threshold.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The Order&#39;s identifier, unique within the Order&#39;s Account. | [optional] 
**create_time** | **str** | The time when the Order was created. | [optional] 
**state** | **str** | The current state of the Order. | [optional] 
**client_extensions** | [**ClientExtensions**](ClientExtensions.md) |  | [optional] 
**type** | **str** | The type of the Order. Always set to \&quot;MARKET_IF_TOUCHED\&quot; for Market If Touched Orders. | [optional] 
**instrument** | **str** | The MarketIfTouched Order&#39;s Instrument. | [optional] 
**units** | **str** | The quantity requested to be filled by the MarketIfTouched Order. A posititive number of units results in a long Order, and a negative number of units results in a short Order. | [optional] 
**price** | **str** | The price threshold specified for the MarketIfTouched Order. The MarketIfTouched Order will only be filled by a market price that crosses this price from the direction of the market price at the time when the Order was created (the initialMarketPrice). Depending on the value of the Order&#39;s price and initialMarketPrice, the MarketIfTouchedOrder will behave like a Limit or a Stop Order. | [optional] 
**price_bound** | **str** | The worst market price that may be used to fill this MarketIfTouched Order. | [optional] 
**time_in_force** | **str** | The time-in-force requested for the MarketIfTouched Order. Restricted to \&quot;GTC\&quot;, \&quot;GFD\&quot; and \&quot;GTD\&quot; for MarketIfTouched Orders. | [optional] 
**gtd_time** | **str** | The date/time when the MarketIfTouched Order will be cancelled if its timeInForce is \&quot;GTD\&quot;. | [optional] 
**position_fill** | **str** | Specification of how Positions in the Account are modified when the Order is filled. | [optional] 
**trigger_condition** | **str** | Specification of which price component should be used when determining if an Order should be triggered and filled. This allows Orders to be triggered based on the bid, ask, mid, default (ask for buy, bid for sell) or inverse (ask for sell, bid for buy) price depending on the desired behaviour. Orders are always filled using their default price component. This feature is only provided through the REST API. Clients who choose to specify a non-default trigger condition will not see it reflected in any of OANDA&#39;s proprietary or partner trading platforms, their transaction history or their account statements. OANDA platforms always assume that an Order&#39;s trigger condition is set to the default value when indicating the distance from an Order&#39;s trigger price, and will always provide the default trigger condition when creating or modifying an Order. A special restriction applies when creating a guaranteed Stop Loss Order. In this case the TriggerCondition value must either be \&quot;DEFAULT\&quot;, or the \&quot;natural\&quot; trigger side \&quot;DEFAULT\&quot; results in. So for a Stop Loss Order for a long trade valid values are \&quot;DEFAULT\&quot; and \&quot;BID\&quot;, and for short trades \&quot;DEFAULT\&quot; and \&quot;ASK\&quot; are valid. | [optional] 
**initial_market_price** | **str** | The Market price at the time when the MarketIfTouched Order was created. | [optional] 
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
**replaces_order_id** | **str** | The ID of the Order that was replaced by this Order (only provided if this Order was created as part of a cancel/replace). | [optional] 
**replaced_by_order_id** | **str** | The ID of the Order that replaced this Order (only provided if this Order was cancelled as part of a cancel/replace). | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.market_if_touched_order import MarketIfTouchedOrder

# TODO update the JSON string below
json = "{}"
# create an instance of MarketIfTouchedOrder from a JSON string
market_if_touched_order_instance = MarketIfTouchedOrder.from_json(json)
# print the JSON string representation of the object
print MarketIfTouchedOrder.to_json()

# convert the object into a dict
market_if_touched_order_dict = market_if_touched_order_instance.to_dict()
# create an instance of MarketIfTouchedOrder from a dict
market_if_touched_order_form_dict = market_if_touched_order.from_dict(market_if_touched_order_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


