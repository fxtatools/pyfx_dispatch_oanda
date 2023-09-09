# Trade

The specification of a Trade within an Account. This includes the full representation of the Trade's dependent Orders in addition to the IDs of those Orders.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The Trade&#39;s identifier, unique within the Trade&#39;s Account. | [optional] 
**instrument** | **str** | The Trade&#39;s Instrument. | [optional] 
**price** | **str** | The execution price of the Trade. | [optional] 
**open_time** | **str** | The date/time when the Trade was opened. | [optional] 
**state** | **str** | The current state of the Trade. | [optional] 
**initial_units** | **str** | The initial size of the Trade. Negative values indicate a short Trade, and positive values indicate a long Trade. | [optional] 
**initial_margin_required** | **str** | The margin required at the time the Trade was created. Note, this is the &#39;pure&#39; margin required, it is not the &#39;effective&#39; margin used that factors in the trade risk if a GSLO is attached to the trade. | [optional] 
**current_units** | **str** | The number of units currently open for the Trade. This value is reduced to 0.0 as the Trade is closed. | [optional] 
**realized_pl** | **str** | The total profit/loss realized on the closed portion of the Trade. | [optional] 
**unrealized_pl** | **str** | The unrealized profit/loss on the open portion of the Trade. | [optional] 
**margin_used** | **str** | Margin currently used by the Trade. | [optional] 
**average_close_price** | **str** | The average closing price of the Trade. Only present if the Trade has been closed or reduced at least once. | [optional] 
**closing_transaction_ids** | **List[str]** | The IDs of the Transactions that have closed portions of this Trade. | [optional] 
**financing** | **str** | The financing paid/collected for this Trade. | [optional] 
**close_time** | **str** | The date/time when the Trade was fully closed. Only provided for Trades whose state is CLOSED. | [optional] 
**client_extensions** | [**ClientExtensions**](ClientExtensions.md) |  | [optional] 
**take_profit_order** | [**TakeProfitOrder**](TakeProfitOrder.md) |  | [optional] 
**stop_loss_order** | [**StopLossOrder**](StopLossOrder.md) |  | [optional] 
**trailing_stop_loss_order** | [**TrailingStopLossOrder**](TrailingStopLossOrder.md) |  | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.trade import Trade

# TODO update the JSON string below
json = "{}"
# create an instance of Trade from a JSON string
trade_instance = Trade.from_json(json)
# print the JSON string representation of the object
print Trade.to_json()

# convert the object into a dict
trade_dict = trade_instance.to_dict()
# create an instance of Trade from a dict
trade_form_dict = trade.from_dict(trade_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


