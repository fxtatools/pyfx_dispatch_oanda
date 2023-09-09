# OrderFillTransaction

An OrderFillTransaction represents the filling of an Order in the client's Account.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The Transaction&#39;s Identifier. | [optional] 
**time** | **str** | The date/time when the Transaction was created. | [optional] 
**user_id** | **int** | The ID of the user that initiated the creation of the Transaction. | [optional] 
**account_id** | **str** | The ID of the Account the Transaction was created for. | [optional] 
**batch_id** | **str** | The ID of the \&quot;batch\&quot; that the Transaction belongs to. Transactions in the same batch are applied to the Account simultaneously. | [optional] 
**request_id** | **str** | The Request ID of the request which generated the transaction. | [optional] 
**type** | **str** | The Type of the Transaction. Always set to \&quot;ORDER_FILL\&quot; for an OrderFillTransaction. | [optional] 
**order_id** | **str** | The ID of the Order filled. | [optional] 
**client_order_id** | **str** | The client Order ID of the Order filled (only provided if the client has assigned one). | [optional] 
**instrument** | **str** | The name of the filled Order&#39;s instrument. | [optional] 
**units** | **str** | The number of units filled by the OrderFill. | [optional] 
**gain_quote_home_conversion_factor** | **str** | This is the conversion factor in effect for the Account at the time of the OrderFill for converting any gains realized in Instrument quote units into units of the Account&#39;s home currency. | [optional] 
**loss_quote_home_conversion_factor** | **str** | This is the conversion factor in effect for the Account at the time of the OrderFill for converting any losses realized in Instrument quote units into units of the Account&#39;s home currency. | [optional] 
**price** | **str** | This field is now deprecated and should no longer be used. The individual tradesClosed, tradeReduced and tradeOpened fields contain the exact/official price each unit was filled at. | [optional] 
**full_vwap** | **str** | The price that all of the units of the OrderFill should have been filled at, in the absence of guaranteed price execution. This factors in the Account&#39;s current ClientPrice, used liquidity and the units of the OrderFill only. If no Trades were closed with their price clamped for guaranteed stop loss enforcement, then this value will match the price fields of each Trade opened, closed, and reduced, and they will all be the exact same. | [optional] 
**full_price** | [**ClientPrice**](ClientPrice.md) |  | [optional] 
**reason** | **str** | The reason that an Order was filled | [optional] 
**pl** | **str** | The profit or loss incurred when the Order was filled. | [optional] 
**financing** | **str** | The financing paid or collected when the Order was filled. | [optional] 
**commission** | **str** | The commission charged in the Account&#39;s home currency as a result of filling the Order. The commission is always represented as a positive quantity of the Account&#39;s home currency, however it reduces the balance in the Account. | [optional] 
**guaranteed_execution_fee** | **str** | The total guaranteed execution fees charged for all Trades opened, closed or reduced with guaranteed Stop Loss Orders. | [optional] 
**account_balance** | **str** | The Account&#39;s balance after the Order was filled. | [optional] 
**trade_opened** | [**TradeOpen**](TradeOpen.md) |  | [optional] 
**trades_closed** | [**List[TradeReduce]**](TradeReduce.md) | The Trades that were closed when the Order was filled (only provided if filling the Order resulted in a closing open Trades). | [optional] 
**trade_reduced** | [**TradeReduce**](TradeReduce.md) |  | [optional] 
**half_spread_cost** | **str** | The half spread cost for the OrderFill, which is the sum of the halfSpreadCost values in the tradeOpened, tradesClosed and tradeReduced fields. This can be a positive or negative value and is represented in the home currency of the Account. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.order_fill_transaction import OrderFillTransaction

# TODO update the JSON string below
json = "{}"
# create an instance of OrderFillTransaction from a JSON string
order_fill_transaction_instance = OrderFillTransaction.from_json(json)
# print the JSON string representation of the object
print OrderFillTransaction.to_json()

# convert the object into a dict
order_fill_transaction_dict = order_fill_transaction_instance.to_dict()
# create an instance of OrderFillTransaction from a dict
order_fill_transaction_form_dict = order_fill_transaction.from_dict(order_fill_transaction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


