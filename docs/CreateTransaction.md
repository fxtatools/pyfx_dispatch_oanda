# CreateTransaction

A CreateTransaction represents the creation of an Account.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The Transaction&#39;s Identifier. | [optional] 
**time** | **str** | The date/time when the Transaction was created. | [optional] 
**user_id** | **int** | The ID of the user that initiated the creation of the Transaction. | [optional] 
**account_id** | **str** | The ID of the Account the Transaction was created for. | [optional] 
**batch_id** | **str** | The ID of the \&quot;batch\&quot; that the Transaction belongs to. Transactions in the same batch are applied to the Account simultaneously. | [optional] 
**request_id** | **str** | The Request ID of the request which generated the transaction. | [optional] 
**type** | **str** | The Type of the Transaction. Always set to \&quot;CREATE\&quot; in a CreateTransaction. | [optional] 
**division_id** | **int** | The ID of the Division that the Account is in | [optional] 
**site_id** | **int** | The ID of the Site that the Account was created at | [optional] 
**account_user_id** | **int** | The ID of the user that the Account was created for | [optional] 
**account_number** | **int** | The number of the Account within the site/division/user | [optional] 
**home_currency** | **str** | The home currency of the Account | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.create_transaction import CreateTransaction

# TODO update the JSON string below
json = "{}"
# create an instance of CreateTransaction from a JSON string
create_transaction_instance = CreateTransaction.from_json(json)
# print the JSON string representation of the object
print CreateTransaction.to_json()

# convert the object into a dict
create_transaction_dict = create_transaction_instance.to_dict()
# create an instance of CreateTransaction from a dict
create_transaction_form_dict = create_transaction.from_dict(create_transaction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


