# MarketOrderTransaction

A MarketOrderTransaction represents the creation of a Market Order in the user's account. A Market Order is an Order that is filled immediately at the current market price. Market Orders can be specialized when they are created to accomplish a specific task: to close a Trade, to closeout a Position or to particiate in in a Margin closeout.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The Transaction&#39;s Identifier. | [optional] 
**time** | **str** | The date/time when the Transaction was created. | [optional] 
**user_id** | **int** | The ID of the user that initiated the creation of the Transaction. | [optional] 
**account_id** | **str** | The ID of the Account the Transaction was created for. | [optional] 
**batch_id** | **str** | The ID of the \&quot;batch\&quot; that the Transaction belongs to. Transactions in the same batch are applied to the Account simultaneously. | [optional] 
**request_id** | **str** | The Request ID of the request which generated the transaction. | [optional] 
**type** | **str** | The Type of the Transaction. Always set to \&quot;MARKET_ORDER\&quot; in a MarketOrderTransaction. | [optional] 
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
**reason** | **str** | The reason that the Market Order was created | [optional] 
**client_extensions** | [**ClientExtensions**](ClientExtensions.md) |  | [optional] 
**take_profit_on_fill** | [**TakeProfitDetails**](TakeProfitDetails.md) |  | [optional] 
**stop_loss_on_fill** | [**StopLossDetails**](StopLossDetails.md) |  | [optional] 
**trailing_stop_loss_on_fill** | [**TrailingStopLossDetails**](TrailingStopLossDetails.md) |  | [optional] 
**trade_client_extensions** | [**ClientExtensions**](ClientExtensions.md) |  | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.market_order_transaction import MarketOrderTransaction

# TODO update the JSON string below
json = "{}"
# create an instance of MarketOrderTransaction from a JSON string
market_order_transaction_instance = MarketOrderTransaction.from_json(json)
# print the JSON string representation of the object
print MarketOrderTransaction.to_json()

# convert the object into a dict
market_order_transaction_dict = market_order_transaction_instance.to_dict()
# create an instance of MarketOrderTransaction from a dict
market_order_transaction_form_dict = market_order_transaction.from_dict(market_order_transaction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


