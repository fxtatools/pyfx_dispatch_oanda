# AccountChangesState

An AccountState Object is used to represent an Account's current price-dependent state. Price-dependent Account state is dependent on OANDA's current Prices, and includes things like unrealized PL, NAV and Trailing Stop Loss Order state.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
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
**orders** | [**List[DynamicOrderState]**](DynamicOrderState.md) | The price-dependent state of each pending Order in the Account. | [optional] 
**trades** | [**List[CalculatedTradeState]**](CalculatedTradeState.md) | The price-dependent state for each open Trade in the Account. | [optional] 
**positions** | [**List[CalculatedPositionState]**](CalculatedPositionState.md) | The price-dependent state for each open Position in the Account. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.account_changes_state import AccountChangesState

# TODO update the JSON string below
json = "{}"
# create an instance of AccountChangesState from a JSON string
account_changes_state_instance = AccountChangesState.from_json(json)
# print the JSON string representation of the object
print AccountChangesState.to_json()

# convert the object into a dict
account_changes_state_dict = account_changes_state_instance.to_dict()
# create an instance of AccountChangesState from a dict
account_changes_state_form_dict = account_changes_state.from_dict(account_changes_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


