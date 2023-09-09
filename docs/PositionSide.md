# PositionSide

The representation of a Position for a single direction (long or short).

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**units** | **str** | Number of units in the position (negative value indicates short position, positive indicates long position). | [optional] 
**average_price** | **str** | Volume-weighted average of the underlying Trade open prices for the Position. | [optional] 
**trade_ids** | **List[str]** | List of the open Trade IDs which contribute to the open Position. | [optional] 
**pl** | **str** | Profit/loss realized by the PositionSide over the lifetime of the Account. | [optional] 
**unrealized_pl** | **str** | The unrealized profit/loss of all open Trades that contribute to this PositionSide. | [optional] 
**resettable_pl** | **str** | Profit/loss realized by the PositionSide since the Account&#39;s resettablePL was last reset by the client. | [optional] 
**financing** | **str** | The total amount of financing paid/collected for this PositionSide over the lifetime of the Account. | [optional] 
**guaranteed_execution_fees** | **str** | The total amount of fees charged over the lifetime of the Account for the execution of guaranteed Stop Loss Orders attached to Trades for this PositionSide. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.position_side import PositionSide

# TODO update the JSON string below
json = "{}"
# create an instance of PositionSide from a JSON string
position_side_instance = PositionSide.from_json(json)
# print the JSON string representation of the object
print PositionSide.to_json()

# convert the object into a dict
position_side_dict = position_side_instance.to_dict()
# create an instance of PositionSide from a dict
position_side_form_dict = position_side.from_dict(position_side_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


