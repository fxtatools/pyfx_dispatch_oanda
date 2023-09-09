# TrailingStopLossOrderRequest

A TrailingStopLossOrderRequest specifies the parameters that may be set when creating a Trailing Stop Loss Order.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The type of the Order to Create. Must be set to \&quot;TRAILING_STOP_LOSS\&quot; when creating a Trailng Stop Loss Order. | [optional] 
**trade_id** | **str** | The ID of the Trade to close when the price threshold is breached. | [optional] 
**client_trade_id** | **str** | The client ID of the Trade to be closed when the price threshold is breached. | [optional] 
**distance** | **str** | The price distance (in price units) specified for the TrailingStopLoss Order. | [optional] 
**time_in_force** | **str** | The time-in-force requested for the TrailingStopLoss Order. Restricted to \&quot;GTC\&quot;, \&quot;GFD\&quot; and \&quot;GTD\&quot; for TrailingStopLoss Orders. | [optional] 
**gtd_time** | **str** | The date/time when the StopLoss Order will be cancelled if its timeInForce is \&quot;GTD\&quot;. | [optional] 
**trigger_condition** | **str** | Specification of which price component should be used when determining if an Order should be triggered and filled. This allows Orders to be triggered based on the bid, ask, mid, default (ask for buy, bid for sell) or inverse (ask for sell, bid for buy) price depending on the desired behaviour. Orders are always filled using their default price component. This feature is only provided through the REST API. Clients who choose to specify a non-default trigger condition will not see it reflected in any of OANDA&#39;s proprietary or partner trading platforms, their transaction history or their account statements. OANDA platforms always assume that an Order&#39;s trigger condition is set to the default value when indicating the distance from an Order&#39;s trigger price, and will always provide the default trigger condition when creating or modifying an Order. A special restriction applies when creating a guaranteed Stop Loss Order. In this case the TriggerCondition value must either be \&quot;DEFAULT\&quot;, or the \&quot;natural\&quot; trigger side \&quot;DEFAULT\&quot; results in. So for a Stop Loss Order for a long trade valid values are \&quot;DEFAULT\&quot; and \&quot;BID\&quot;, and for short trades \&quot;DEFAULT\&quot; and \&quot;ASK\&quot; are valid. | [optional] 
**client_extensions** | [**ClientExtensions**](ClientExtensions.md) |  | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.trailing_stop_loss_order_request import TrailingStopLossOrderRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TrailingStopLossOrderRequest from a JSON string
trailing_stop_loss_order_request_instance = TrailingStopLossOrderRequest.from_json(json)
# print the JSON string representation of the object
print TrailingStopLossOrderRequest.to_json()

# convert the object into a dict
trailing_stop_loss_order_request_dict = trailing_stop_loss_order_request_instance.to_dict()
# create an instance of TrailingStopLossOrderRequest from a dict
trailing_stop_loss_order_request_form_dict = trailing_stop_loss_order_request.from_dict(trailing_stop_loss_order_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


