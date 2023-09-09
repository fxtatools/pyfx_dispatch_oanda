# ClosePosition400Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**long_order_reject_transaction** | [**MarketOrderRejectTransaction**](MarketOrderRejectTransaction.md) |  | [optional] 
**short_order_reject_transaction** | [**MarketOrderRejectTransaction**](MarketOrderRejectTransaction.md) |  | [optional] 
**related_transaction_ids** | **List[str]** | The IDs of all Transactions that were created while satisfying the request. | [optional] 
**last_transaction_id** | **str** | The ID of the most recent Transaction created for the Account | [optional] 
**error_code** | **str** | The code of the error that has occurred. This field may not be returned for some errors. | [optional] 
**error_message** | **str** | The human-readable description of the error that has occurred. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.close_position400_response import ClosePosition400Response

# TODO update the JSON string below
json = "{}"
# create an instance of ClosePosition400Response from a JSON string
close_position400_response_instance = ClosePosition400Response.from_json(json)
# print the JSON string representation of the object
print ClosePosition400Response.to_json()

# convert the object into a dict
close_position400_response_dict = close_position400_response_instance.to_dict()
# create an instance of ClosePosition400Response from a dict
close_position400_response_form_dict = close_position400_response.from_dict(close_position400_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


