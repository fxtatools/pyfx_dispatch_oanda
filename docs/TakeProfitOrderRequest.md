# TakeProfitOrderRequest

A TakeProfitOrderRequest specifies the parameters that may be set when creating a Take Profit Order. Only one of the price and distance fields may be specified.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The type of the Order to Create. Must be set to \&quot;TAKE_PROFIT\&quot; when creating a Take Profit Order. | [optional] 
**trade_id** | **str** | The ID of the Trade to close when the price threshold is breached. | [optional] 
**client_trade_id** | **str** | The client ID of the Trade to be closed when the price threshold is breached. | [optional] 
**price** | **str** | The price threshold specified for the TakeProfit Order. The associated Trade will be closed by a market price that is equal to or better than this threshold. | [optional] 
**time_in_force** | **str** | The time-in-force requested for the TakeProfit Order. Restricted to \&quot;GTC\&quot;, \&quot;GFD\&quot; and \&quot;GTD\&quot; for TakeProfit Orders. | [optional] 
**gtd_time** | **str** | The date/time when the TakeProfit Order will be cancelled if its timeInForce is \&quot;GTD\&quot;. | [optional] 
**trigger_condition** | **str** | Specification of which price component should be used when determining if an Order should be triggered and filled. This allows Orders to be triggered based on the bid, ask, mid, default (ask for buy, bid for sell) or inverse (ask for sell, bid for buy) price depending on the desired behaviour. Orders are always filled using their default price component. This feature is only provided through the REST API. Clients who choose to specify a non-default trigger condition will not see it reflected in any of OANDA&#39;s proprietary or partner trading platforms, their transaction history or their account statements. OANDA platforms always assume that an Order&#39;s trigger condition is set to the default value when indicating the distance from an Order&#39;s trigger price, and will always provide the default trigger condition when creating or modifying an Order. A special restriction applies when creating a guaranteed Stop Loss Order. In this case the TriggerCondition value must either be \&quot;DEFAULT\&quot;, or the \&quot;natural\&quot; trigger side \&quot;DEFAULT\&quot; results in. So for a Stop Loss Order for a long trade valid values are \&quot;DEFAULT\&quot; and \&quot;BID\&quot;, and for short trades \&quot;DEFAULT\&quot; and \&quot;ASK\&quot; are valid. | [optional] 
**client_extensions** | [**ClientExtensions**](ClientExtensions.md) |  | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.take_profit_order_request import TakeProfitOrderRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TakeProfitOrderRequest from a JSON string
take_profit_order_request_instance = TakeProfitOrderRequest.from_json(json)
# print the JSON string representation of the object
print TakeProfitOrderRequest.to_json()

# convert the object into a dict
take_profit_order_request_dict = take_profit_order_request_instance.to_dict()
# create an instance of TakeProfitOrderRequest from a dict
take_profit_order_request_form_dict = take_profit_order_request.from_dict(take_profit_order_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


