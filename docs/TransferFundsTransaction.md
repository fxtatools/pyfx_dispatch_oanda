# TransferFundsTransaction

A TransferFundsTransaction represents the transfer of funds in/out of an Account.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The Transaction&#39;s Identifier. | [optional] 
**time** | **str** | The date/time when the Transaction was created. | [optional] 
**user_id** | **int** | The ID of the user that initiated the creation of the Transaction. | [optional] 
**account_id** | **str** | The ID of the Account the Transaction was created for. | [optional] 
**batch_id** | **str** | The ID of the \&quot;batch\&quot; that the Transaction belongs to. Transactions in the same batch are applied to the Account simultaneously. | [optional] 
**request_id** | **str** | The Request ID of the request which generated the transaction. | [optional] 
**type** | **str** | The Type of the Transaction. Always set to \&quot;TRANSFER_FUNDS\&quot; in a TransferFundsTransaction. | [optional] 
**amount** | **str** | The amount to deposit/withdraw from the Account in the Account&#39;s home currency. A positive value indicates a deposit, a negative value indicates a withdrawal. | [optional] 
**funding_reason** | **str** | The reason that an Account is being funded. | [optional] 
**comment** | **str** | An optional comment that may be attached to a fund transfer for audit purposes | [optional] 
**account_balance** | **str** | The Account&#39;s balance after funds are transferred. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.transfer_funds_transaction import TransferFundsTransaction

# TODO update the JSON string below
json = "{}"
# create an instance of TransferFundsTransaction from a JSON string
transfer_funds_transaction_instance = TransferFundsTransaction.from_json(json)
# print the JSON string representation of the object
print TransferFundsTransaction.to_json()

# convert the object into a dict
transfer_funds_transaction_dict = transfer_funds_transaction_instance.to_dict()
# create an instance of TransferFundsTransaction from a dict
transfer_funds_transaction_form_dict = transfer_funds_transaction.from_dict(transfer_funds_transaction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


