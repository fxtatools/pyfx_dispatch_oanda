# PriceBucket

A Price Bucket represents a price available for an amount of liquidity

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**price** | **str** | The Price offered by the PriceBucket | [optional] 
**liquidity** | **int** | The amount of liquidity offered by the PriceBucket | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.price_bucket import PriceBucket

# TODO update the JSON string below
json = "{}"
# create an instance of PriceBucket from a JSON string
price_bucket_instance = PriceBucket.from_json(json)
# print the JSON string representation of the object
print PriceBucket.to_json()

# convert the object into a dict
price_bucket_dict = price_bucket_instance.to_dict()
# create an instance of PriceBucket from a dict
price_bucket_form_dict = price_bucket.from_dict(price_bucket_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


