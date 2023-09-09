# InstrumentCommission

An InstrumentCommission represents an instrument-specific commission

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**commission** | **str** | The commission amount (in the Account&#39;s home currency) charged per unitsTraded of the instrument | [optional] 
**units_traded** | **str** | The number of units traded that the commission amount is based on. | [optional] 
**minimum_commission** | **str** | The minimum commission amount (in the Account&#39;s home currency) that is charged when an Order is filled for this instrument. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.instrument_commission import InstrumentCommission

# TODO update the JSON string below
json = "{}"
# create an instance of InstrumentCommission from a JSON string
instrument_commission_instance = InstrumentCommission.from_json(json)
# print the JSON string representation of the object
print InstrumentCommission.to_json()

# convert the object into a dict
instrument_commission_dict = instrument_commission_instance.to_dict()
# create an instance of InstrumentCommission from a dict
instrument_commission_form_dict = instrument_commission.from_dict(instrument_commission_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


