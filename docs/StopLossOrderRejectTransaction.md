# StopLossOrderRejectTransaction

A StopLossOrderRejectTransaction represents the rejection of the creation of a StopLoss Order.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The Transaction&#39;s Identifier. | [optional] 
**time** | **str** | The date/time when the Transaction was created. | [optional] 
**user_id** | **int** | The ID of the user that initiated the creation of the Transaction. | [optional] 
**account_id** | **str** | The ID of the Account the Transaction was created for. | [optional] 
**batch_id** | **str** | The ID of the \&quot;batch\&quot; that the Transaction belongs to. Transactions in the same batch are applied to the Account simultaneously. | [optional] 
**request_id** | **str** | The Request ID of the request which generated the transaction. | [optional] 
**type** | **str** | The Type of the Transaction. Always set to \&quot;STOP_LOSS_ORDER_REJECT\&quot; in a StopLossOrderRejectTransaction. | [optional] 
**trade_id** | **str** | The ID of the Trade to close when the price threshold is breached. | [optional] 
**client_trade_id** | **str** | The client ID of the Trade to be closed when the price threshold is breached. | [optional] 
**price** | **str** | The price threshold specified for the Stop Loss Order. If the guaranteed flag is false, the associated Trade will be closed by a market price that is equal to or worse than this threshold. If the flag is true the associated Trade will be closed at this price. | [optional] 
**distance** | **str** | Specifies the distance (in price units) from the Account&#39;s current price to use as the Stop Loss Order price. If the Trade is short the Instrument&#39;s bid price is used, and for long Trades the ask is used. | [optional] 
**time_in_force** | **str** | The time-in-force requested for the StopLoss Order. Restricted to \&quot;GTC\&quot;, \&quot;GFD\&quot; and \&quot;GTD\&quot; for StopLoss Orders. | [optional] 
**gtd_time** | **str** | The date/time when the StopLoss Order will be cancelled if its timeInForce is \&quot;GTD\&quot;. | [optional] 
**trigger_condition** | **str** | Specification of which price component should be used when determining if an Order should be triggered and filled. This allows Orders to be triggered based on the bid, ask, mid, default (ask for buy, bid for sell) or inverse (ask for sell, bid for buy) price depending on the desired behaviour. Orders are always filled using their default price component. This feature is only provided through the REST API. Clients who choose to specify a non-default trigger condition will not see it reflected in any of OANDA&#39;s proprietary or partner trading platforms, their transaction history or their account statements. OANDA platforms always assume that an Order&#39;s trigger condition is set to the default value when indicating the distance from an Order&#39;s trigger price, and will always provide the default trigger condition when creating or modifying an Order. A special restriction applies when creating a guaranteed Stop Loss Order. In this case the TriggerCondition value must either be \&quot;DEFAULT\&quot;, or the \&quot;natural\&quot; trigger side \&quot;DEFAULT\&quot; results in. So for a Stop Loss Order for a long trade valid values are \&quot;DEFAULT\&quot; and \&quot;BID\&quot;, and for short trades \&quot;DEFAULT\&quot; and \&quot;ASK\&quot; are valid. | [optional] 
**guaranteed** | **bool** | Flag indicating that the Stop Loss Order is guaranteed. The default value depends on the GuaranteedStopLossOrderMode of the account, if it is REQUIRED, the default will be true, for DISABLED or ENABLED the default is false. | [optional] 
**reason** | **str** | The reason that the Stop Loss Order was initiated | [optional] 
**client_extensions** | [**ClientExtensions**](ClientExtensions.md) |  | [optional] 
**order_fill_transaction_id** | **str** | The ID of the OrderFill Transaction that caused this Order to be created (only provided if this Order was created automatically when another Order was filled). | [optional] 
**intended_replaces_order_id** | **str** | The ID of the Order that this Order was intended to replace (only provided if this Order was intended to replace an existing Order). | [optional] 
**reject_reason** | **str** | The reason that the Reject Transaction was created | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.stop_loss_order_reject_transaction import StopLossOrderRejectTransaction

# TODO update the JSON string below
json = "{}"
# create an instance of StopLossOrderRejectTransaction from a JSON string
stop_loss_order_reject_transaction_instance = StopLossOrderRejectTransaction.from_json(json)
# print the JSON string representation of the object
print StopLossOrderRejectTransaction.to_json()

# convert the object into a dict
stop_loss_order_reject_transaction_dict = stop_loss_order_reject_transaction_instance.to_dict()
# create an instance of StopLossOrderRejectTransaction from a dict
stop_loss_order_reject_transaction_form_dict = stop_loss_order_reject_transaction.from_dict(stop_loss_order_reject_transaction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


