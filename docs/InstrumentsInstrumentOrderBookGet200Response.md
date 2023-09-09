# InstrumentsInstrumentOrderBookGet200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_book** | [**OrderBook**](OrderBook.md) |  | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.instruments_instrument_order_book_get200_response import InstrumentsInstrumentOrderBookGet200Response

# TODO update the JSON string below
json = "{}"
# create an instance of InstrumentsInstrumentOrderBookGet200Response from a JSON string
instruments_instrument_order_book_get200_response_instance = InstrumentsInstrumentOrderBookGet200Response.from_json(json)
# print the JSON string representation of the object
print InstrumentsInstrumentOrderBookGet200Response.to_json()

# convert the object into a dict
instruments_instrument_order_book_get200_response_dict = instruments_instrument_order_book_get200_response_instance.to_dict()
# create an instance of InstrumentsInstrumentOrderBookGet200Response from a dict
instruments_instrument_order_book_get200_response_form_dict = instruments_instrument_order_book_get200_response.from_dict(instruments_instrument_order_book_get200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


