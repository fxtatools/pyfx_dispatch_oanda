# ClosePositionRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**long_units** | **str** | Indication of how much of the long Position to closeout. Either the string \&quot;ALL\&quot;, the string \&quot;NONE\&quot;, or a DecimalNumber representing how many units of the long position to close using a PositionCloseout MarketOrder. The units specified must always be positive. | [optional] 
**long_client_extensions** | [**ClientExtensions**](ClientExtensions.md) |  | [optional] 
**short_units** | **str** | Indication of how much of the short Position to closeout. Either the string \&quot;ALL\&quot;, the string \&quot;NONE\&quot;, or a DecimalNumber representing how many units of the short position to close using a PositionCloseout MarketOrder. The units specified must always be positive. | [optional] 
**short_client_extensions** | [**ClientExtensions**](ClientExtensions.md) |  | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.close_position_request import ClosePositionRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ClosePositionRequest from a JSON string
close_position_request_instance = ClosePositionRequest.from_json(json)
# print the JSON string representation of the object
print ClosePositionRequest.to_json()

# convert the object into a dict
close_position_request_dict = close_position_request_instance.to_dict()
# create an instance of ClosePositionRequest from a dict
close_position_request_form_dict = close_position_request.from_dict(close_position_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


