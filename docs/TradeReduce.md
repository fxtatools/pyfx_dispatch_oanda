# TradeReduce

A TradeReduce object represents a Trade for an instrument that was reduced (either partially or fully) in an Account. It is found embedded in Transactions that affect the position of an instrument in the account, specifically the OrderFill Transaction.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**trade_id** | **str** | The ID of the Trade that was reduced or closed | [optional] 
**units** | **str** | The number of units that the Trade was reduced by | [optional] 
**price** | **str** | The average price that the units were closed at. This price may be clamped for guaranteed Stop Loss Orders. | [optional] 
**realized_pl** | **str** | The PL realized when reducing the Trade | [optional] 
**financing** | **str** | The financing paid/collected when reducing the Trade | [optional] 
**guaranteed_execution_fee** | **str** | This is the fee that is charged for closing the Trade if it has a guaranteed Stop Loss Order attached to it. | [optional] 
**half_spread_cost** | **str** | The half spread cost for the trade reduce/close. This can be a positive or negative value and is represented in the home currency of the Account. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.trade_reduce import TradeReduce

# TODO update the JSON string below
json = "{}"
# create an instance of TradeReduce from a JSON string
trade_reduce_instance = TradeReduce.from_json(json)
# print the JSON string representation of the object
print TradeReduce.to_json()

# convert the object into a dict
trade_reduce_dict = trade_reduce_instance.to_dict()
# create an instance of TradeReduce from a dict
trade_reduce_form_dict = trade_reduce.from_dict(trade_reduce_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


