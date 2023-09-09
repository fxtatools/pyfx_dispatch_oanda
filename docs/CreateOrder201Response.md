# CreateOrder201Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_create_transaction** | [**Transaction**](Transaction.md) |  | [optional] 
**order_fill_transaction** | [**OrderFillTransaction**](OrderFillTransaction.md) |  | [optional] 
**order_cancel_transaction** | [**OrderCancelTransaction**](OrderCancelTransaction.md) |  | [optional] 
**order_reissue_transaction** | [**Transaction**](Transaction.md) |  | [optional] 
**order_reissue_reject_transaction** | [**Transaction**](Transaction.md) |  | [optional] 
**related_transaction_ids** | **List[str]** | The IDs of all Transactions that were created while satisfying the request. | [optional] 
**last_transaction_id** | **str** | The ID of the most recent Transaction created for the Account | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.create_order201_response import CreateOrder201Response

# TODO update the JSON string below
json = "{}"
# create an instance of CreateOrder201Response from a JSON string
create_order201_response_instance = CreateOrder201Response.from_json(json)
# print the JSON string representation of the object
print CreateOrder201Response.to_json()

# convert the object into a dict
create_order201_response_dict = create_order201_response_instance.to_dict()
# create an instance of CreateOrder201Response from a dict
create_order201_response_form_dict = create_order201_response.from_dict(create_order201_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


