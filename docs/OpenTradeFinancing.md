# OpenTradeFinancing

OpenTradeFinancing is used to pay/collect daily financing charge for an open Trade within an Account

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**trade_id** | **str** | The ID of the Trade that financing is being paid/collected for. | [optional] 
**financing** | **str** | The amount of financing paid/collected for the Trade. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.open_trade_financing import OpenTradeFinancing

# TODO update the JSON string below
json = "{}"
# create an instance of OpenTradeFinancing from a JSON string
open_trade_financing_instance = OpenTradeFinancing.from_json(json)
# print the JSON string representation of the object
print OpenTradeFinancing.to_json()

# convert the object into a dict
open_trade_financing_dict = open_trade_financing_instance.to_dict()
# create an instance of OpenTradeFinancing from a dict
open_trade_financing_form_dict = open_trade_financing.from_dict(open_trade_financing_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


