# GetExternalUserInfo200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_info** | [**UserInfoExternal**](UserInfoExternal.md) |  | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.get_external_user_info200_response import GetExternalUserInfo200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetExternalUserInfo200Response from a JSON string
get_external_user_info200_response_instance = GetExternalUserInfo200Response.from_json(json)
# print the JSON string representation of the object
print GetExternalUserInfo200Response.to_json()

# convert the object into a dict
get_external_user_info200_response_dict = get_external_user_info200_response_instance.to_dict()
# create an instance of GetExternalUserInfo200Response from a dict
get_external_user_info200_response_form_dict = get_external_user_info200_response.from_dict(get_external_user_info200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


