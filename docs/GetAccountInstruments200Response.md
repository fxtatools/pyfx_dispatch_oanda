# GetAccountInstruments200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**instruments** | [**List[Instrument]**](Instrument.md) | The requested list of instruments. | [optional] 
**last_transaction_id** | **str** | The ID of the most recent Transaction created for the Account. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.get_account_instruments200_response import GetAccountInstruments200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetAccountInstruments200Response from a JSON string
get_account_instruments200_response_instance = GetAccountInstruments200Response.from_json(json)
# print the JSON string representation of the object
print GetAccountInstruments200Response.to_json()

# convert the object into a dict
get_account_instruments200_response_dict = get_account_instruments200_response_instance.to_dict()
# create an instance of GetAccountInstruments200Response from a dict
get_account_instruments200_response_form_dict = get_account_instruments200_response.from_dict(get_account_instruments200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


