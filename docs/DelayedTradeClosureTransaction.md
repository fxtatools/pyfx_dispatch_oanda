# DelayedTradeClosureTransaction

A DelayedTradeClosure Transaction is created administratively to indicate open trades that should have been closed but weren't because the open trades' instruments were untradeable at the time. Open trades listed in this transaction will be closed once their respective instruments become tradeable.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The Transaction&#39;s Identifier. | [optional] 
**time** | **str** | The date/time when the Transaction was created. | [optional] 
**user_id** | **int** | The ID of the user that initiated the creation of the Transaction. | [optional] 
**account_id** | **str** | The ID of the Account the Transaction was created for. | [optional] 
**batch_id** | **str** | The ID of the \&quot;batch\&quot; that the Transaction belongs to. Transactions in the same batch are applied to the Account simultaneously. | [optional] 
**request_id** | **str** | The Request ID of the request which generated the transaction. | [optional] 
**type** | **str** | The Type of the Transaction. Always set to \&quot;DELAYED_TRADE_CLOSURE\&quot; for an DelayedTradeClosureTransaction. | [optional] 
**reason** | **str** | The reason for the delayed trade closure | [optional] 
**trade_ids** | **str** | List of Trade ID&#39;s identifying the open trades that will be closed when their respective instruments become tradeable | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.delayed_trade_closure_transaction import DelayedTradeClosureTransaction

# TODO update the JSON string below
json = "{}"
# create an instance of DelayedTradeClosureTransaction from a JSON string
delayed_trade_closure_transaction_instance = DelayedTradeClosureTransaction.from_json(json)
# print the JSON string representation of the object
print DelayedTradeClosureTransaction.to_json()

# convert the object into a dict
delayed_trade_closure_transaction_dict = delayed_trade_closure_transaction_instance.to_dict()
# create an instance of DelayedTradeClosureTransaction from a dict
delayed_trade_closure_transaction_form_dict = delayed_trade_closure_transaction.from_dict(delayed_trade_closure_transaction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


