# UserInfo

A representation of user information, as provided to the user themself.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**username** | **str** | The user-provided username. | [optional] 
**user_id** | **int** | The user&#39;s OANDA-assigned user ID. | [optional] 
**country** | **str** | The country that the user is based in. | [optional] 
**email_address** | **str** | The user&#39;s email address. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.user_info import UserInfo

# TODO update the JSON string below
json = "{}"
# create an instance of UserInfo from a JSON string
user_info_instance = UserInfo.from_json(json)
# print the JSON string representation of the object
print UserInfo.to_json()

# convert the object into a dict
user_info_dict = user_info_instance.to_dict()
# create an instance of UserInfo from a dict
user_info_form_dict = user_info.from_dict(user_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


