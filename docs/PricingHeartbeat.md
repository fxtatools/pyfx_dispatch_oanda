# PricingHeartbeat

A PricingHeartbeat object is injected into the Pricing stream to ensure that the HTTP connection remains active.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The string \&quot;HEARTBEAT\&quot; | [optional] 
**time** | **str** | The date/time when the Heartbeat was created. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.pricing_heartbeat import PricingHeartbeat

# TODO update the JSON string below
json = "{}"
# create an instance of PricingHeartbeat from a JSON string
pricing_heartbeat_instance = PricingHeartbeat.from_json(json)
# print the JSON string representation of the object
print PricingHeartbeat.to_json()

# convert the object into a dict
pricing_heartbeat_dict = pricing_heartbeat_instance.to_dict()
# create an instance of PricingHeartbeat from a dict
pricing_heartbeat_form_dict = pricing_heartbeat.from_dict(pricing_heartbeat_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


