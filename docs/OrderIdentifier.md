# OrderIdentifier

An OrderIdentifier is used to refer to an Order, and contains both the OrderID and the ClientOrderID.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_id** | **str** | The OANDA-assigned Order ID | [optional] 
**client_order_id** | **str** | The client-provided client Order ID | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.order_identifier import OrderIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of OrderIdentifier from a JSON string
order_identifier_instance = OrderIdentifier.from_json(json)
# print the JSON string representation of the object
print OrderIdentifier.to_json()

# convert the object into a dict
order_identifier_dict = order_identifier_instance.to_dict()
# create an instance of OrderIdentifier from a dict
order_identifier_form_dict = order_identifier.from_dict(order_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


