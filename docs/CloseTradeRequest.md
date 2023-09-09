# CloseTradeRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**units** | **str** | Indication of how much of the Trade to close. Either the string \&quot;ALL\&quot; (indicating that all of the Trade should be closed), or a DecimalNumber representing the number of units of the open Trade to Close using a TradeClose MarketOrder. The units specified must always be positive, and the magnitude of the value cannot exceed the magnitude of the Trade&#39;s open units. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.close_trade_request import CloseTradeRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CloseTradeRequest from a JSON string
close_trade_request_instance = CloseTradeRequest.from_json(json)
# print the JSON string representation of the object
print CloseTradeRequest.to_json()

# convert the object into a dict
close_trade_request_dict = close_trade_request_instance.to_dict()
# create an instance of CloseTradeRequest from a dict
close_trade_request_form_dict = close_trade_request.from_dict(close_trade_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


