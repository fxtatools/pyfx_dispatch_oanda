# StreamTransactions200Response

The response body for the Transaction Stream uses chunked transfer encoding.  Each chunk contains Transaction and/or TransactionHeartbeat objects encoded as JSON.  Each JSON object is serialized into a single line of text, and multiple objects found in the same chunk are separated by newlines. TransactionHeartbeats are sent every 5 seconds.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction** | [**Transaction**](Transaction.md) |  | [optional] 
**heartbeat** | [**TransactionHeartbeat**](TransactionHeartbeat.md) |  | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.stream_transactions200_response import StreamTransactions200Response

# TODO update the JSON string below
json = "{}"
# create an instance of StreamTransactions200Response from a JSON string
stream_transactions200_response_instance = StreamTransactions200Response.from_json(json)
# print the JSON string representation of the object
print StreamTransactions200Response.to_json()

# convert the object into a dict
stream_transactions200_response_dict = stream_transactions200_response_instance.to_dict()
# create an instance of StreamTransactions200Response from a dict
stream_transactions200_response_form_dict = stream_transactions200_response.from_dict(stream_transactions200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


