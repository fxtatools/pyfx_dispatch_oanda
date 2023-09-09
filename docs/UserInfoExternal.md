# UserInfoExternal

A representation of user information, as available to external (3rd party) clients.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **int** | The user&#39;s OANDA-assigned user ID. | [optional] 
**country** | **str** | The country that the user is based in. | [optional] 
**fifo** | **bool** | Flag indicating if the the user&#39;s Accounts adhere to FIFO execution rules. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.user_info_external import UserInfoExternal

# TODO update the JSON string below
json = "{}"
# create an instance of UserInfoExternal from a JSON string
user_info_external_instance = UserInfoExternal.from_json(json)
# print the JSON string representation of the object
print UserInfoExternal.to_json()

# convert the object into a dict
user_info_external_dict = user_info_external_instance.to_dict()
# create an instance of UserInfoExternal from a dict
user_info_external_form_dict = user_info_external.from_dict(user_info_external_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


