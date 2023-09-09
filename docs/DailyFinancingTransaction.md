# DailyFinancingTransaction

A DailyFinancingTransaction represents the daily payment/collection of financing for an Account.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The Transaction&#39;s Identifier. | [optional] 
**time** | **str** | The date/time when the Transaction was created. | [optional] 
**user_id** | **int** | The ID of the user that initiated the creation of the Transaction. | [optional] 
**account_id** | **str** | The ID of the Account the Transaction was created for. | [optional] 
**batch_id** | **str** | The ID of the \&quot;batch\&quot; that the Transaction belongs to. Transactions in the same batch are applied to the Account simultaneously. | [optional] 
**request_id** | **str** | The Request ID of the request which generated the transaction. | [optional] 
**type** | **str** | The Type of the Transaction. Always set to \&quot;DAILY_FINANCING\&quot; for a DailyFinancingTransaction. | [optional] 
**financing** | **str** | The amount of financing paid/collected for the Account. | [optional] 
**account_balance** | **str** | The Account&#39;s balance after daily financing. | [optional] 
**account_financing_mode** | **str** | The account financing mode at the time of the daily financing. | [optional] 
**position_financings** | [**List[PositionFinancing]**](PositionFinancing.md) | The financing paid/collected for each Position in the Account. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.daily_financing_transaction import DailyFinancingTransaction

# TODO update the JSON string below
json = "{}"
# create an instance of DailyFinancingTransaction from a JSON string
daily_financing_transaction_instance = DailyFinancingTransaction.from_json(json)
# print the JSON string representation of the object
print DailyFinancingTransaction.to_json()

# convert the object into a dict
daily_financing_transaction_dict = daily_financing_transaction_instance.to_dict()
# create an instance of DailyFinancingTransaction from a dict
daily_financing_transaction_form_dict = daily_financing_transaction.from_dict(daily_financing_transaction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


