# AccountChanges

An AccountChanges Object is used to represent the changes to an Account's Orders, Trades and Positions since a specified Account TransactionID in the past.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**orders_created** | [**List[Order]**](Order.md) | The Orders created. These Orders may have been filled, cancelled or triggered in the same period. | [optional] 
**orders_cancelled** | [**List[Order]**](Order.md) | The Orders cancelled. | [optional] 
**orders_filled** | [**List[Order]**](Order.md) | The Orders filled. | [optional] 
**orders_triggered** | [**List[Order]**](Order.md) | The Orders triggered. | [optional] 
**trades_opened** | [**List[TradeSummary]**](TradeSummary.md) | The Trades opened. | [optional] 
**trades_reduced** | [**List[TradeSummary]**](TradeSummary.md) | The Trades reduced. | [optional] 
**trades_closed** | [**List[TradeSummary]**](TradeSummary.md) | The Trades closed. | [optional] 
**positions** | [**List[Position]**](Position.md) | The Positions changed. | [optional] 
**transactions** | [**List[Transaction]**](Transaction.md) | The Transactions that have been generated. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.account_changes import AccountChanges

# TODO update the JSON string below
json = "{}"
# create an instance of AccountChanges from a JSON string
account_changes_instance = AccountChanges.from_json(json)
# print the JSON string representation of the object
print AccountChanges.to_json()

# convert the object into a dict
account_changes_dict = account_changes_instance.to_dict()
# create an instance of AccountChanges from a dict
account_changes_form_dict = account_changes.from_dict(account_changes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


