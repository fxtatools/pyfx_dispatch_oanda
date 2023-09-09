# Account

The full details of a client's Account. This includes full open Trade, open Position and pending Order representation.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The Account&#39;s identifier | [optional] 
**alias** | **str** | Client-assigned alias for the Account. Only provided if the Account has an alias set | [optional] 
**currency** | **str** | The home currency of the Account | [optional] 
**balance** | **str** | The current balance of the Account. | [optional] 
**created_by_user_id** | **int** | ID of the user that created the Account. | [optional] 
**created_time** | **str** | The date/time when the Account was created. | [optional] 
**guaranteed_stop_loss_order_mode** | **str** | The current guaranteed Stop Loss Order mode of the Account. | [optional] 
**pl** | **str** | The total profit/loss realized over the lifetime of the Account. | [optional] 
**resettable_pl** | **str** | The total realized profit/loss for the Account since it was last reset by the client. | [optional] 
**resettable_pl_time** | **str** | The date/time that the Account&#39;s resettablePL was last reset. | [optional] 
**financing** | **str** | The total amount of financing paid/collected over the lifetime of the Account. | [optional] 
**commission** | **str** | The total amount of commission paid over the lifetime of the Account. | [optional] 
**guaranteed_execution_fees** | **str** | The total amount of fees charged over the lifetime of the Account for the execution of guaranteed Stop Loss Orders. | [optional] 
**margin_rate** | **str** | Client-provided margin rate override for the Account. The effective margin rate of the Account is the lesser of this value and the OANDA margin rate for the Account&#39;s division. This value is only provided if a margin rate override exists for the Account. | [optional] 
**margin_call_enter_time** | **str** | The date/time when the Account entered a margin call state. Only provided if the Account is in a margin call. | [optional] 
**margin_call_extension_count** | **int** | The number of times that the Account&#39;s current margin call was extended. | [optional] 
**last_margin_call_extension_time** | **str** | The date/time of the Account&#39;s last margin call extension. | [optional] 
**open_trade_count** | **int** | The number of Trades currently open in the Account. | [optional] 
**open_position_count** | **int** | The number of Positions currently open in the Account. | [optional] 
**pending_order_count** | **int** | The number of Orders currently pending in the Account. | [optional] 
**hedging_enabled** | **bool** | Flag indicating that the Account has hedging enabled. | [optional] 
**last_order_fill_timestamp** | **str** | The date/time of the last order that was filled for this account. | [optional] 
**unrealized_pl** | **str** | The total unrealized profit/loss for all Trades currently open in the Account. | [optional] 
**nav** | **str** | The net asset value of the Account. Equal to Account balance + unrealizedPL. | [optional] 
**margin_used** | **str** | Margin currently used for the Account. | [optional] 
**margin_available** | **str** | Margin available for Account currency. | [optional] 
**position_value** | **str** | The value of the Account&#39;s open positions represented in the Account&#39;s home currency. | [optional] 
**margin_closeout_unrealized_pl** | **str** | The Account&#39;s margin closeout unrealized PL. | [optional] 
**margin_closeout_nav** | **str** | The Account&#39;s margin closeout NAV. | [optional] 
**margin_closeout_margin_used** | **str** | The Account&#39;s margin closeout margin used. | [optional] 
**margin_closeout_percent** | **str** | The Account&#39;s margin closeout percentage. When this value is 1.0 or above the Account is in a margin closeout situation. | [optional] 
**margin_closeout_position_value** | **str** | The value of the Account&#39;s open positions as used for margin closeout calculations represented in the Account&#39;s home currency. | [optional] 
**withdrawal_limit** | **str** | The current WithdrawalLimit for the account which will be zero or a positive value indicating how much can be withdrawn from the account. | [optional] 
**margin_call_margin_used** | **str** | The Account&#39;s margin call margin used. | [optional] 
**margin_call_percent** | **str** | The Account&#39;s margin call percentage. When this value is 1.0 or above the Account is in a margin call situation. | [optional] 
**last_transaction_id** | **str** | The ID of the last Transaction created for the Account. | [optional] 
**trades** | [**List[TradeSummary]**](TradeSummary.md) | The details of the Trades currently open in the Account. | [optional] 
**positions** | [**List[Position]**](Position.md) | The details all Account Positions. | [optional] 
**orders** | [**List[Order]**](Order.md) | The details of the Orders currently pending in the Account. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.account import Account

# TODO update the JSON string below
json = "{}"
# create an instance of Account from a JSON string
account_instance = Account.from_json(json)
# print the JSON string representation of the object
print Account.to_json()

# convert the object into a dict
account_dict = account_instance.to_dict()
# create an instance of Account from a dict
account_form_dict = account.from_dict(account_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


