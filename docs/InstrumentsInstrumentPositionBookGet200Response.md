# InstrumentsInstrumentPositionBookGet200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**position_book** | [**PositionBook**](PositionBook.md) |  | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.instruments_instrument_position_book_get200_response import InstrumentsInstrumentPositionBookGet200Response

# TODO update the JSON string below
json = "{}"
# create an instance of InstrumentsInstrumentPositionBookGet200Response from a JSON string
instruments_instrument_position_book_get200_response_instance = InstrumentsInstrumentPositionBookGet200Response.from_json(json)
# print the JSON string representation of the object
print InstrumentsInstrumentPositionBookGet200Response.to_json()

# convert the object into a dict
instruments_instrument_position_book_get200_response_dict = instruments_instrument_position_book_get200_response_instance.to_dict()
# create an instance of InstrumentsInstrumentPositionBookGet200Response from a dict
instruments_instrument_position_book_get200_response_form_dict = instruments_instrument_position_book_get200_response.from_dict(instruments_instrument_position_book_get200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


