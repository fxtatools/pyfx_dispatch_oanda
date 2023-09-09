# CloseTrade400Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_reject_transaction** | [**MarketOrderRejectTransaction**](MarketOrderRejectTransaction.md) |  | [optional] 
**error_code** | **str** | The code of the error that has occurred. This field may not be returned for some errors. | [optional] 
**error_message** | **str** | The human-readable description of the error that has occurred. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.close_trade400_response import CloseTrade400Response

# TODO update the JSON string below
json = "{}"
# create an instance of CloseTrade400Response from a JSON string
close_trade400_response_instance = CloseTrade400Response.from_json(json)
# print the JSON string representation of the object
print CloseTrade400Response.to_json()

# convert the object into a dict
close_trade400_response_dict = close_trade400_response_instance.to_dict()
# create an instance of CloseTrade400Response from a dict
close_trade400_response_form_dict = close_trade400_response.from_dict(close_trade400_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


