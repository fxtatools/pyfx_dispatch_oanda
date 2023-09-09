# AccountProperties

Properties related to an Account.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The Account&#39;s identifier | [optional] 
**mt4_account_id** | **int** | The Account&#39;s associated MT4 Account ID. This field will not be present if the Account is not an MT4 account. | [optional] 
**tags** | **List[str]** | The Account&#39;s tags | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.account_properties import AccountProperties

# TODO update the JSON string below
json = "{}"
# create an instance of AccountProperties from a JSON string
account_properties_instance = AccountProperties.from_json(json)
# print the JSON string representation of the object
print AccountProperties.to_json()

# convert the object into a dict
account_properties_dict = account_properties_instance.to_dict()
# create an instance of AccountProperties from a dict
account_properties_form_dict = account_properties.from_dict(account_properties_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


