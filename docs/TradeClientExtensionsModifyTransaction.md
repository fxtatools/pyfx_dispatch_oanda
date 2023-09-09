# TradeClientExtensionsModifyTransaction

A TradeClientExtensionsModifyTransaction represents the modification of a Trade's Client Extensions.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The Transaction&#39;s Identifier. | [optional] 
**time** | **str** | The date/time when the Transaction was created. | [optional] 
**user_id** | **int** | The ID of the user that initiated the creation of the Transaction. | [optional] 
**account_id** | **str** | The ID of the Account the Transaction was created for. | [optional] 
**batch_id** | **str** | The ID of the \&quot;batch\&quot; that the Transaction belongs to. Transactions in the same batch are applied to the Account simultaneously. | [optional] 
**request_id** | **str** | The Request ID of the request which generated the transaction. | [optional] 
**type** | **str** | The Type of the Transaction. Always set to \&quot;TRADE_CLIENT_EXTENSIONS_MODIFY\&quot; for a TradeClientExtensionsModifyTransaction. | [optional] 
**trade_id** | **str** | The ID of the Trade who&#39;s client extensions are to be modified. | [optional] 
**client_trade_id** | **str** | The original Client ID of the Trade who&#39;s client extensions are to be modified. | [optional] 
**trade_client_extensions_modify** | [**ClientExtensions**](ClientExtensions.md) |  | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.trade_client_extensions_modify_transaction import TradeClientExtensionsModifyTransaction

# TODO update the JSON string below
json = "{}"
# create an instance of TradeClientExtensionsModifyTransaction from a JSON string
trade_client_extensions_modify_transaction_instance = TradeClientExtensionsModifyTransaction.from_json(json)
# print the JSON string representation of the object
print TradeClientExtensionsModifyTransaction.to_json()

# convert the object into a dict
trade_client_extensions_modify_transaction_dict = trade_client_extensions_modify_transaction_instance.to_dict()
# create an instance of TradeClientExtensionsModifyTransaction from a dict
trade_client_extensions_modify_transaction_form_dict = trade_client_extensions_modify_transaction.from_dict(trade_client_extensions_modify_transaction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


