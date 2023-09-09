# TakeProfitOrder

A TakeProfitOrder is an order that is linked to an open Trade and created with a price threshold. The Order will be filled (closing the Trade) by the first price that is equal to or better than the threshold. A TakeProfitOrder cannot be used to open a new Position.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The Order&#39;s identifier, unique within the Order&#39;s Account. | [optional] 
**create_time** | **str** | The time when the Order was created. | [optional] 
**state** | **str** | The current state of the Order. | [optional] 
**client_extensions** | [**ClientExtensions**](ClientExtensions.md) |  | [optional] 
**type** | **str** | The type of the Order. Always set to \&quot;TAKE_PROFIT\&quot; for Take Profit Orders. | [optional] 
**trade_id** | **str** | The ID of the Trade to close when the price threshold is breached. | [optional] 
**client_trade_id** | **str** | The client ID of the Trade to be closed when the price threshold is breached. | [optional] 
**price** | **str** | The price threshold specified for the TakeProfit Order. The associated Trade will be closed by a market price that is equal to or better than this threshold. | [optional] 
**time_in_force** | **str** | The time-in-force requested for the TakeProfit Order. Restricted to \&quot;GTC\&quot;, \&quot;GFD\&quot; and \&quot;GTD\&quot; for TakeProfit Orders. | [optional] 
**gtd_time** | **str** | The date/time when the TakeProfit Order will be cancelled if its timeInForce is \&quot;GTD\&quot;. | [optional] 
**trigger_condition** | **str** | Specification of which price component should be used when determining if an Order should be triggered and filled. This allows Orders to be triggered based on the bid, ask, mid, default (ask for buy, bid for sell) or inverse (ask for sell, bid for buy) price depending on the desired behaviour. Orders are always filled using their default price component. This feature is only provided through the REST API. Clients who choose to specify a non-default trigger condition will not see it reflected in any of OANDA&#39;s proprietary or partner trading platforms, their transaction history or their account statements. OANDA platforms always assume that an Order&#39;s trigger condition is set to the default value when indicating the distance from an Order&#39;s trigger price, and will always provide the default trigger condition when creating or modifying an Order. A special restriction applies when creating a guaranteed Stop Loss Order. In this case the TriggerCondition value must either be \&quot;DEFAULT\&quot;, or the \&quot;natural\&quot; trigger side \&quot;DEFAULT\&quot; results in. So for a Stop Loss Order for a long trade valid values are \&quot;DEFAULT\&quot; and \&quot;BID\&quot;, and for short trades \&quot;DEFAULT\&quot; and \&quot;ASK\&quot; are valid. | [optional] 
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
from pyfx.dispatch.oanda.models.take_profit_order import TakeProfitOrder

# TODO update the JSON string below
json = "{}"
# create an instance of TakeProfitOrder from a JSON string
take_profit_order_instance = TakeProfitOrder.from_json(json)
# print the JSON string representation of the object
print TakeProfitOrder.to_json()

# convert the object into a dict
take_profit_order_dict = take_profit_order_instance.to_dict()
# create an instance of TakeProfitOrder from a dict
take_profit_order_form_dict = take_profit_order.from_dict(take_profit_order_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


