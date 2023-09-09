# OrderBookBucket

The order book data for a partition of the instrument's prices.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**price** | **str** | The lowest price (inclusive) covered by the bucket. The bucket covers the price range from the price to price + the order book&#39;s bucketWidth. | [optional] 
**long_count_percent** | **str** | The percentage of the total number of orders represented by the long orders found in this bucket. | [optional] 
**short_count_percent** | **str** | The percentage of the total number of orders represented by the short orders found in this bucket. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.order_book_bucket import OrderBookBucket

# TODO update the JSON string below
json = "{}"
# create an instance of OrderBookBucket from a JSON string
order_book_bucket_instance = OrderBookBucket.from_json(json)
# print the JSON string representation of the object
print OrderBookBucket.to_json()

# convert the object into a dict
order_book_bucket_dict = order_book_bucket_instance.to_dict()
# create an instance of OrderBookBucket from a dict
order_book_bucket_form_dict = order_book_bucket.from_dict(order_book_bucket_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


