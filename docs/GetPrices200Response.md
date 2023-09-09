# GetPrices200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prices** | [**List[ClientPrice]**](ClientPrice.md) | The list of Price objects requested. | [optional] 
**home_conversions** | [**List[HomeConversions]**](HomeConversions.md) | The list of home currency conversion factors requested. This field will only be present if includeHomeConversions was set to true in the request. | [optional] 
**time** | **str** | The DateTime value to use for the \&quot;since\&quot; parameter in the next poll request. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.get_prices200_response import GetPrices200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetPrices200Response from a JSON string
get_prices200_response_instance = GetPrices200Response.from_json(json)
# print the JSON string representation of the object
print GetPrices200Response.to_json()

# convert the object into a dict
get_prices200_response_dict = get_prices200_response_instance.to_dict()
# create an instance of GetPrices200Response from a dict
get_prices200_response_form_dict = get_prices200_response.from_dict(get_prices200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


