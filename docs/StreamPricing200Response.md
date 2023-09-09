# StreamPricing200Response

The response body for the Pricing Stream uses chunked transfer encoding.  Each chunk contains Price and/or PricingHeartbeat objects encoded as JSON.  Each JSON object is serialized into a single line of text, and multiple objects found in the same chunk are separated by newlines. Heartbeats are sent every 5 seconds.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**price** | [**ClientPrice**](ClientPrice.md) |  | [optional] 
**heartbeat** | [**PricingHeartbeat**](PricingHeartbeat.md) |  | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.stream_pricing200_response import StreamPricing200Response

# TODO update the JSON string below
json = "{}"
# create an instance of StreamPricing200Response from a JSON string
stream_pricing200_response_instance = StreamPricing200Response.from_json(json)
# print the JSON string representation of the object
print StreamPricing200Response.to_json()

# convert the object into a dict
stream_pricing200_response_dict = stream_pricing200_response_instance.to_dict()
# create an instance of StreamPricing200Response from a dict
stream_pricing200_response_form_dict = stream_pricing200_response.from_dict(stream_pricing200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


