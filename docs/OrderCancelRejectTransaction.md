# OrderCancelRejectTransaction

An OrderCancelRejectTransaction represents the rejection of the cancellation of an Order in the client's Account.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The Transaction&#39;s Identifier. | [optional] 
**time** | **str** | The date/time when the Transaction was created. | [optional] 
**user_id** | **int** | The ID of the user that initiated the creation of the Transaction. | [optional] 
**account_id** | **str** | The ID of the Account the Transaction was created for. | [optional] 
**batch_id** | **str** | The ID of the \&quot;batch\&quot; that the Transaction belongs to. Transactions in the same batch are applied to the Account simultaneously. | [optional] 
**request_id** | **str** | The Request ID of the request which generated the transaction. | [optional] 
**type** | **str** | The Type of the Transaction. Always set to \&quot;ORDER_CANCEL_REJECT\&quot; for an OrderCancelRejectTransaction. | [optional] 
**order_id** | **str** | The ID of the Order intended to be cancelled | [optional] 
**client_order_id** | **str** | The client ID of the Order intended to be cancelled (only provided if the Order has a client Order ID). | [optional] 
**reject_reason** | **str** | The reason that the Reject Transaction was created | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.order_cancel_reject_transaction import OrderCancelRejectTransaction

# TODO update the JSON string below
json = "{}"
# create an instance of OrderCancelRejectTransaction from a JSON string
order_cancel_reject_transaction_instance = OrderCancelRejectTransaction.from_json(json)
# print the JSON string representation of the object
print OrderCancelRejectTransaction.to_json()

# convert the object into a dict
order_cancel_reject_transaction_dict = order_cancel_reject_transaction_instance.to_dict()
# create an instance of OrderCancelRejectTransaction from a dict
order_cancel_reject_transaction_form_dict = order_cancel_reject_transaction.from_dict(order_cancel_reject_transaction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


