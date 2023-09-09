# PositionBookBucket

The position book data for a partition of the instrument's prices.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**price** | **str** | The lowest price (inclusive) covered by the bucket. The bucket covers the price range from the price to price + the position book&#39;s bucketWidth. | [optional] 
**long_count_percent** | **str** | The percentage of the total number of positions represented by the long positions found in this bucket. | [optional] 
**short_count_percent** | **str** | The percentage of the total number of positions represented by the short positions found in this bucket. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.position_book_bucket import PositionBookBucket

# TODO update the JSON string below
json = "{}"
# create an instance of PositionBookBucket from a JSON string
position_book_bucket_instance = PositionBookBucket.from_json(json)
# print the JSON string representation of the object
print PositionBookBucket.to_json()

# convert the object into a dict
position_book_bucket_dict = position_book_bucket_instance.to_dict()
# create an instance of PositionBookBucket from a dict
position_book_bucket_form_dict = position_book_bucket.from_dict(position_book_bucket_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


