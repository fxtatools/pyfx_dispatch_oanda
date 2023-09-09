# ReplaceOrder201Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_cancel_transaction** | [**OrderCancelTransaction**](OrderCancelTransaction.md) |  | [optional] 
**order_create_transaction** | [**Transaction**](Transaction.md) |  | [optional] 
**order_fill_transaction** | [**OrderFillTransaction**](OrderFillTransaction.md) |  | [optional] 
**order_reissue_transaction** | [**Transaction**](Transaction.md) |  | [optional] 
**order_reissue_reject_transaction** | [**Transaction**](Transaction.md) |  | [optional] 
**replacing_order_cancel_transaction** | [**OrderCancelTransaction**](OrderCancelTransaction.md) |  | [optional] 
**related_transaction_ids** | **List[str]** | The IDs of all Transactions that were created while satisfying the request. | [optional] 
**last_transaction_id** | **str** | The ID of the most recent Transaction created for the Account | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.replace_order201_response import ReplaceOrder201Response

# TODO update the JSON string below
json = "{}"
# create an instance of ReplaceOrder201Response from a JSON string
replace_order201_response_instance = ReplaceOrder201Response.from_json(json)
# print the JSON string representation of the object
print ReplaceOrder201Response.to_json()

# convert the object into a dict
replace_order201_response_dict = replace_order201_response_instance.to_dict()
# create an instance of ReplaceOrder201Response from a dict
replace_order201_response_form_dict = replace_order201_response.from_dict(replace_order201_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


