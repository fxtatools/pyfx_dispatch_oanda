# UnitsAvailableDetails

Representation of many units of an Instrument are available to be traded for both long and short Orders.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**long** | **str** | The units available for long Orders. | [optional] 
**short** | **str** | The units available for short Orders. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.units_available_details import UnitsAvailableDetails

# TODO update the JSON string below
json = "{}"
# create an instance of UnitsAvailableDetails from a JSON string
units_available_details_instance = UnitsAvailableDetails.from_json(json)
# print the JSON string representation of the object
print UnitsAvailableDetails.to_json()

# convert the object into a dict
units_available_details_dict = units_available_details_instance.to_dict()
# create an instance of UnitsAvailableDetails from a dict
units_available_details_form_dict = units_available_details.from_dict(units_available_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


