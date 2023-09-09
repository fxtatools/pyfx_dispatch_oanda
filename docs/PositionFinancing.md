# PositionFinancing

OpenTradeFinancing is used to pay/collect daily financing charge for a Position within an Account

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**instrument** | **str** | The instrument of the Position that financing is being paid/collected for. | [optional] 
**financing** | **str** | The amount of financing paid/collected for the Position. | [optional] 
**open_trade_financings** | [**List[OpenTradeFinancing]**](OpenTradeFinancing.md) | The financing paid/collecte for each open Trade within the Position. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.position_financing import PositionFinancing

# TODO update the JSON string below
json = "{}"
# create an instance of PositionFinancing from a JSON string
position_financing_instance = PositionFinancing.from_json(json)
# print the JSON string representation of the object
print PositionFinancing.to_json()

# convert the object into a dict
position_financing_dict = position_financing_instance.to_dict()
# create an instance of PositionFinancing from a dict
position_financing_form_dict = position_financing.from_dict(position_financing_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


