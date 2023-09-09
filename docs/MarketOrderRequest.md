# MarketOrderRequest

A MarketOrderRequest specifies the parameters that may be set when creating a Market Order.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The type of the Order to Create. Must be set to \&quot;MARKET\&quot; when creating a Market Order. | [optional] 
**instrument** | **str** | The Market Order&#39;s Instrument. | [optional] 
**units** | **str** | The quantity requested to be filled by the Market Order. A posititive number of units results in a long Order, and a negative number of units results in a short Order. | [optional] 
**time_in_force** | **str** | The time-in-force requested for the Market Order. Restricted to FOK or IOC for a MarketOrder. | [optional] 
**price_bound** | **str** | The worst price that the client is willing to have the Market Order filled at. | [optional] 
**position_fill** | **str** | Specification of how Positions in the Account are modified when the Order is filled. | [optional] 
**client_extensions** | [**ClientExtensions**](ClientExtensions.md) |  | [optional] 
**take_profit_on_fill** | [**TakeProfitDetails**](TakeProfitDetails.md) |  | [optional] 
**stop_loss_on_fill** | [**StopLossDetails**](StopLossDetails.md) |  | [optional] 
**trailing_stop_loss_on_fill** | [**TrailingStopLossDetails**](TrailingStopLossDetails.md) |  | [optional] 
**trade_client_extensions** | [**ClientExtensions**](ClientExtensions.md) |  | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.market_order_request import MarketOrderRequest

# TODO update the JSON string below
json = "{}"
# create an instance of MarketOrderRequest from a JSON string
market_order_request_instance = MarketOrderRequest.from_json(json)
# print the JSON string representation of the object
print MarketOrderRequest.to_json()

# convert the object into a dict
market_order_request_dict = market_order_request_instance.to_dict()
# create an instance of MarketOrderRequest from a dict
market_order_request_form_dict = market_order_request.from_dict(market_order_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


