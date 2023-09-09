# FixedPriceOrderTransaction

A FixedPriceOrderTransaction represents the creation of a Fixed Price Order in the user's account. A Fixed Price Order is an Order that is filled immediately at a specified price.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The Transaction&#39;s Identifier. | [optional] 
**time** | **str** | The date/time when the Transaction was created. | [optional] 
**user_id** | **int** | The ID of the user that initiated the creation of the Transaction. | [optional] 
**account_id** | **str** | The ID of the Account the Transaction was created for. | [optional] 
**batch_id** | **str** | The ID of the \&quot;batch\&quot; that the Transaction belongs to. Transactions in the same batch are applied to the Account simultaneously. | [optional] 
**request_id** | **str** | The Request ID of the request which generated the transaction. | [optional] 
**type** | **str** | The Type of the Transaction. Always set to \&quot;FIXED_PRICE_ORDER\&quot; in a FixedPriceOrderTransaction. | [optional] 
**instrument** | **str** | The Fixed Price Order&#39;s Instrument. | [optional] 
**units** | **str** | The quantity requested to be filled by the Fixed Price Order. A posititive number of units results in a long Order, and a negative number of units results in a short Order. | [optional] 
**price** | **str** | The price specified for the Fixed Price Order. This price is the exact price that the Fixed Price Order will be filled at. | [optional] 
**position_fill** | **str** | Specification of how Positions in the Account are modified when the Order is filled. | [optional] 
**trade_state** | **str** | The state that the trade resulting from the Fixed Price Order should be set to. | [optional] 
**reason** | **str** | The reason that the Fixed Price Order was created | [optional] 
**client_extensions** | [**ClientExtensions**](ClientExtensions.md) |  | [optional] 
**take_profit_on_fill** | [**TakeProfitDetails**](TakeProfitDetails.md) |  | [optional] 
**stop_loss_on_fill** | [**StopLossDetails**](StopLossDetails.md) |  | [optional] 
**trailing_stop_loss_on_fill** | [**TrailingStopLossDetails**](TrailingStopLossDetails.md) |  | [optional] 
**trade_client_extensions** | [**ClientExtensions**](ClientExtensions.md) |  | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.fixed_price_order_transaction import FixedPriceOrderTransaction

# TODO update the JSON string below
json = "{}"
# create an instance of FixedPriceOrderTransaction from a JSON string
fixed_price_order_transaction_instance = FixedPriceOrderTransaction.from_json(json)
# print the JSON string representation of the object
print FixedPriceOrderTransaction.to_json()

# convert the object into a dict
fixed_price_order_transaction_dict = fixed_price_order_transaction_instance.to_dict()
# create an instance of FixedPriceOrderTransaction from a dict
fixed_price_order_transaction_form_dict = fixed_price_order_transaction.from_dict(fixed_price_order_transaction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


