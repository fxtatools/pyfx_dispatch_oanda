# CreateOrderRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order** | **object** | The base Order specification used when requesting that an Order be created. Each specific Order-type extends this definition. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.create_order_request import CreateOrderRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateOrderRequest from a JSON string
create_order_request_instance = CreateOrderRequest.from_json(json)
# print the JSON string representation of the object
print CreateOrderRequest.to_json()

# convert the object into a dict
create_order_request_dict = create_order_request_instance.to_dict()
# create an instance of CreateOrderRequest from a dict
create_order_request_form_dict = create_order_request.from_dict(create_order_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


