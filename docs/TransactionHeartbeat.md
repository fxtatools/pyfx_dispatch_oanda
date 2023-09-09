# TransactionHeartbeat

A TransactionHeartbeat object is injected into the Transaction stream to ensure that the HTTP connection remains active.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The string \&quot;HEARTBEAT\&quot; | [optional] 
**last_transaction_id** | **str** | The ID of the most recent Transaction created for the Account | [optional] 
**time** | **str** | The date/time when the TransactionHeartbeat was created. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.transaction_heartbeat import TransactionHeartbeat

# TODO update the JSON string below
json = "{}"
# create an instance of TransactionHeartbeat from a JSON string
transaction_heartbeat_instance = TransactionHeartbeat.from_json(json)
# print the JSON string representation of the object
print TransactionHeartbeat.to_json()

# convert the object into a dict
transaction_heartbeat_dict = transaction_heartbeat_instance.to_dict()
# create an instance of TransactionHeartbeat from a dict
transaction_heartbeat_form_dict = transaction_heartbeat.from_dict(transaction_heartbeat_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


