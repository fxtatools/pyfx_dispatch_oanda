# UnitsAvailable

Representation of how many units of an Instrument are available to be traded by an Order depending on its postionFill option.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**default** | [**UnitsAvailableDetails**](UnitsAvailableDetails.md) |  | [optional] 
**reduce_first** | [**UnitsAvailableDetails**](UnitsAvailableDetails.md) |  | [optional] 
**reduce_only** | [**UnitsAvailableDetails**](UnitsAvailableDetails.md) |  | [optional] 
**open_only** | [**UnitsAvailableDetails**](UnitsAvailableDetails.md) |  | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.units_available import UnitsAvailable

# TODO update the JSON string below
json = "{}"
# create an instance of UnitsAvailable from a JSON string
units_available_instance = UnitsAvailable.from_json(json)
# print the JSON string representation of the object
print UnitsAvailable.to_json()

# convert the object into a dict
units_available_dict = units_available_instance.to_dict()
# create an instance of UnitsAvailable from a dict
units_available_form_dict = units_available.from_dict(units_available_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


