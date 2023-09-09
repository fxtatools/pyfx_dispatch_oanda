# MT4TransactionHeartbeat

A TransactionHeartbeat object is injected into the Transaction stream to ensure that the HTTP connection remains active.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The string \&quot;HEARTBEAT\&quot; | [optional] 
**time** | **str** | The date/time when the TransactionHeartbeat was created. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.mt4_transaction_heartbeat import MT4TransactionHeartbeat

# TODO update the JSON string below
json = "{}"
# create an instance of MT4TransactionHeartbeat from a JSON string
mt4_transaction_heartbeat_instance = MT4TransactionHeartbeat.from_json(json)
# print the JSON string representation of the object
print MT4TransactionHeartbeat.to_json()

# convert the object into a dict
mt4_transaction_heartbeat_dict = mt4_transaction_heartbeat_instance.to_dict()
# create an instance of MT4TransactionHeartbeat from a dict
mt4_transaction_heartbeat_form_dict = mt4_transaction_heartbeat.from_dict(mt4_transaction_heartbeat_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


