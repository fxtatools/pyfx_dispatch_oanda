# SetTradeClientExtensions200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**trade_client_extensions_modify_transaction** | [**TradeClientExtensionsModifyTransaction**](TradeClientExtensionsModifyTransaction.md) |  | [optional] 
**related_transaction_ids** | **List[str]** | The IDs of all Transactions that were created while satisfying the request. | [optional] 
**last_transaction_id** | **str** | The ID of the most recent Transaction created for the Account | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.set_trade_client_extensions200_response import SetTradeClientExtensions200Response

# TODO update the JSON string below
json = "{}"
# create an instance of SetTradeClientExtensions200Response from a JSON string
set_trade_client_extensions200_response_instance = SetTradeClientExtensions200Response.from_json(json)
# print the JSON string representation of the object
print SetTradeClientExtensions200Response.to_json()

# convert the object into a dict
set_trade_client_extensions200_response_dict = set_trade_client_extensions200_response_instance.to_dict()
# create an instance of SetTradeClientExtensions200Response from a dict
set_trade_client_extensions200_response_form_dict = set_trade_client_extensions200_response.from_dict(set_trade_client_extensions200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


