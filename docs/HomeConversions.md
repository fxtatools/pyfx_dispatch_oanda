# HomeConversions

HomeConversions represents the factors to use to convert quantities of a given currency into the Account's home currency. The conversion factor depends on the scenario the conversion is required for.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**currency** | **str** | The currency to be converted into the home currency. | [optional] 
**account_gain** | **str** | The factor used to convert any gains for an Account in the specified currency into the Account&#39;s home currency. This would include positive realized P/L and positive financing amounts. Conversion is performed by multiplying the positive P/L by the conversion factor. | [optional] 
**account_loss** | **str** | The string representation of a decimal number. | [optional] 
**position_value** | **str** | The factor used to convert a Position or Trade Value in the specified currency into the Account&#39;s home currency. Conversion is performed by multiplying the Position or Trade Value by the conversion factor. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.home_conversions import HomeConversions

# TODO update the JSON string below
json = "{}"
# create an instance of HomeConversions from a JSON string
home_conversions_instance = HomeConversions.from_json(json)
# print the JSON string representation of the object
print HomeConversions.to_json()

# convert the object into a dict
home_conversions_dict = home_conversions_instance.to_dict()
# create an instance of HomeConversions from a dict
home_conversions_form_dict = home_conversions.from_dict(home_conversions_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


