# LimitOrderRequest

A LimitOrderRequest specifies the parameters that may be set when creating a Limit Order.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The type of the Order to Create. Must be set to \&quot;LIMIT\&quot; when creating a Market Order. | [optional] 
**instrument** | **str** | The Limit Order&#39;s Instrument. | [optional] 
**units** | **str** | The quantity requested to be filled by the Limit Order. A posititive number of units results in a long Order, and a negative number of units results in a short Order. | [optional] 
**price** | **str** | The price threshold specified for the Limit Order. The Limit Order will only be filled by a market price that is equal to or better than this price. | [optional] 
**time_in_force** | **str** | The time-in-force requested for the Limit Order. | [optional] 
**gtd_time** | **str** | The date/time when the Limit Order will be cancelled if its timeInForce is \&quot;GTD\&quot;. | [optional] 
**position_fill** | **str** | Specification of how Positions in the Account are modified when the Order is filled. | [optional] 
**trigger_condition** | **str** | Specification of which price component should be used when determining if an Order should be triggered and filled. This allows Orders to be triggered based on the bid, ask, mid, default (ask for buy, bid for sell) or inverse (ask for sell, bid for buy) price depending on the desired behaviour. Orders are always filled using their default price component. This feature is only provided through the REST API. Clients who choose to specify a non-default trigger condition will not see it reflected in any of OANDA&#39;s proprietary or partner trading platforms, their transaction history or their account statements. OANDA platforms always assume that an Order&#39;s trigger condition is set to the default value when indicating the distance from an Order&#39;s trigger price, and will always provide the default trigger condition when creating or modifying an Order. A special restriction applies when creating a guaranteed Stop Loss Order. In this case the TriggerCondition value must either be \&quot;DEFAULT\&quot;, or the \&quot;natural\&quot; trigger side \&quot;DEFAULT\&quot; results in. So for a Stop Loss Order for a long trade valid values are \&quot;DEFAULT\&quot; and \&quot;BID\&quot;, and for short trades \&quot;DEFAULT\&quot; and \&quot;ASK\&quot; are valid. | [optional] 
**client_extensions** | [**ClientExtensions**](ClientExtensions.md) |  | [optional] 
**take_profit_on_fill** | [**TakeProfitDetails**](TakeProfitDetails.md) |  | [optional] 
**stop_loss_on_fill** | [**StopLossDetails**](StopLossDetails.md) |  | [optional] 
**trailing_stop_loss_on_fill** | [**TrailingStopLossDetails**](TrailingStopLossDetails.md) |  | [optional] 
**trade_client_extensions** | [**ClientExtensions**](ClientExtensions.md) |  | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.limit_order_request import LimitOrderRequest

# TODO update the JSON string below
json = "{}"
# create an instance of LimitOrderRequest from a JSON string
limit_order_request_instance = LimitOrderRequest.from_json(json)
# print the JSON string representation of the object
print LimitOrderRequest.to_json()

# convert the object into a dict
limit_order_request_dict = limit_order_request_instance.to_dict()
# create an instance of LimitOrderRequest from a dict
limit_order_request_form_dict = limit_order_request.from_dict(limit_order_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


