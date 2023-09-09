# ResetResettablePLTransaction

A ResetResettablePLTransaction represents the resetting of the Account's resettable PL counters.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The Transaction&#39;s Identifier. | [optional] 
**time** | **str** | The date/time when the Transaction was created. | [optional] 
**user_id** | **int** | The ID of the user that initiated the creation of the Transaction. | [optional] 
**account_id** | **str** | The ID of the Account the Transaction was created for. | [optional] 
**batch_id** | **str** | The ID of the \&quot;batch\&quot; that the Transaction belongs to. Transactions in the same batch are applied to the Account simultaneously. | [optional] 
**request_id** | **str** | The Request ID of the request which generated the transaction. | [optional] 
**type** | **str** | The Type of the Transaction. Always set to \&quot;RESET_RESETTABLE_PL\&quot; for a ResetResettablePLTransaction. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.reset_resettable_pl_transaction import ResetResettablePLTransaction

# TODO update the JSON string below
json = "{}"
# create an instance of ResetResettablePLTransaction from a JSON string
reset_resettable_pl_transaction_instance = ResetResettablePLTransaction.from_json(json)
# print the JSON string representation of the object
print ResetResettablePLTransaction.to_json()

# convert the object into a dict
reset_resettable_pl_transaction_dict = reset_resettable_pl_transaction_instance.to_dict()
# create an instance of ResetResettablePLTransaction from a dict
reset_resettable_pl_transaction_form_dict = reset_resettable_pl_transaction.from_dict(reset_resettable_pl_transaction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


