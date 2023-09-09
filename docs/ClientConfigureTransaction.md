# ClientConfigureTransaction

A ClientConfigureTransaction represents the configuration of an Account by a client.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The Transaction&#39;s Identifier. | [optional] 
**time** | **str** | The date/time when the Transaction was created. | [optional] 
**user_id** | **int** | The ID of the user that initiated the creation of the Transaction. | [optional] 
**account_id** | **str** | The ID of the Account the Transaction was created for. | [optional] 
**batch_id** | **str** | The ID of the \&quot;batch\&quot; that the Transaction belongs to. Transactions in the same batch are applied to the Account simultaneously. | [optional] 
**request_id** | **str** | The Request ID of the request which generated the transaction. | [optional] 
**type** | **str** | The Type of the Transaction. Always set to \&quot;CLIENT_CONFIGURE\&quot; in a ClientConfigureTransaction. | [optional] 
**alias** | **str** | The client-provided alias for the Account. | [optional] 
**margin_rate** | **str** | The margin rate override for the Account. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.client_configure_transaction import ClientConfigureTransaction

# TODO update the JSON string below
json = "{}"
# create an instance of ClientConfigureTransaction from a JSON string
client_configure_transaction_instance = ClientConfigureTransaction.from_json(json)
# print the JSON string representation of the object
print ClientConfigureTransaction.to_json()

# convert the object into a dict
client_configure_transaction_dict = client_configure_transaction_instance.to_dict()
# create an instance of ClientConfigureTransaction from a dict
client_configure_transaction_form_dict = client_configure_transaction.from_dict(client_configure_transaction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

