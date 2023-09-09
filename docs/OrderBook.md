# OrderBook

The representation of an instrument's order book at a point in time

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**instrument** | **str** | The order book&#39;s instrument | [optional] 
**time** | **str** | The time when the order book snapshot was created. | [optional] 
**price** | **str** | The price (midpoint) for the order book&#39;s instrument at the time of the order book snapshot | [optional] 
**bucket_width** | **str** | The price width for each bucket. Each bucket covers the price range from the bucket&#39;s price to the bucket&#39;s price + bucketWidth. | [optional] 
**buckets** | [**List[OrderBookBucket]**](OrderBookBucket.md) | The partitioned order book, divided into buckets using a default bucket width. These buckets are only provided for price ranges which actually contain order or position data. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.order_book import OrderBook

# TODO update the JSON string below
json = "{}"
# create an instance of OrderBook from a JSON string
order_book_instance = OrderBook.from_json(json)
# print the JSON string representation of the object
print OrderBook.to_json()

# convert the object into a dict
order_book_dict = order_book_instance.to_dict()
# create an instance of OrderBook from a dict
order_book_form_dict = order_book.from_dict(order_book_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


