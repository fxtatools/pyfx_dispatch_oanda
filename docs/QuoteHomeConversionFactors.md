# QuoteHomeConversionFactors

QuoteHomeConversionFactors represents the factors that can be used used to convert quantities of a Price's Instrument's quote currency into the Account's home currency.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**positive_units** | **str** | The factor used to convert a positive amount of the Price&#39;s Instrument&#39;s quote currency into a positive amount of the Account&#39;s home currency.  Conversion is performed by multiplying the quote units by the conversion factor. | [optional] 
**negative_units** | **str** | The factor used to convert a negative amount of the Price&#39;s Instrument&#39;s quote currency into a negative amount of the Account&#39;s home currency.  Conversion is performed by multiplying the quote units by the conversion factor. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.quote_home_conversion_factors import QuoteHomeConversionFactors

# TODO update the JSON string below
json = "{}"
# create an instance of QuoteHomeConversionFactors from a JSON string
quote_home_conversion_factors_instance = QuoteHomeConversionFactors.from_json(json)
# print the JSON string representation of the object
print QuoteHomeConversionFactors.to_json()

# convert the object into a dict
quote_home_conversion_factors_dict = quote_home_conversion_factors_instance.to_dict()
# create an instance of QuoteHomeConversionFactors from a dict
quote_home_conversion_factors_form_dict = quote_home_conversion_factors.from_dict(quote_home_conversion_factors_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


