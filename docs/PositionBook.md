# PositionBook

The representation of an instrument's position book at a point in time

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**instrument** | **str** | The position book&#39;s instrument | [optional] 
**time** | **str** | The time when the position book snapshot was created | [optional] 
**price** | **str** | The price (midpoint) for the position book&#39;s instrument at the time of the position book snapshot | [optional] 
**bucket_width** | **str** | The price width for each bucket. Each bucket covers the price range from the bucket&#39;s price to the bucket&#39;s price + bucketWidth. | [optional] 
**buckets** | [**List[PositionBookBucket]**](PositionBookBucket.md) | The partitioned position book, divided into buckets using a default bucket width. These buckets are only provided for price ranges which actually contain order or position data. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.position_book import PositionBook

# TODO update the JSON string below
json = "{}"
# create an instance of PositionBook from a JSON string
position_book_instance = PositionBook.from_json(json)
# print the JSON string representation of the object
print PositionBook.to_json()

# convert the object into a dict
position_book_dict = position_book_instance.to_dict()
# create an instance of PositionBook from a dict
position_book_form_dict = position_book.from_dict(position_book_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


