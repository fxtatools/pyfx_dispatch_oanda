# Price

The Price representation

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**instrument** | **str** | The Price&#39;s Instrument. | [optional] 
**tradeable** | **bool** | Flag indicating if the Price is tradeable or not | [optional] 
**timestamp** | **str** | The date/time when the Price was created. | [optional] 
**base_bid** | **str** | The base bid price as calculated by pricing. | [optional] 
**base_ask** | **str** | The base ask price as calculated by pricing. | [optional] 
**bids** | [**List[PriceBucket]**](PriceBucket.md) | The list of prices and liquidity available on the Instrument&#39;s bid side. It is possible for this list to be empty if there is no bid liquidity currently available for the Instrument in the Account. | [optional] 
**asks** | [**List[PriceBucket]**](PriceBucket.md) | The list of prices and liquidity available on the Instrument&#39;s ask side. It is possible for this list to be empty if there is no ask liquidity currently available for the Instrument in the Account. | [optional] 
**closeout_bid** | **str** | The closeout bid price. This price is used when a bid is required to closeout a Position (margin closeout or manual) yet there is no bid liquidity. The closeout bid is never used to open a new position. | [optional] 
**closeout_ask** | **str** | The closeout ask price. This price is used when an ask is required to closeout a Position (margin closeout or manual) yet there is no ask liquidity. The closeout ask is never used to open a new position. | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.price import Price

# TODO update the JSON string below
json = "{}"
# create an instance of Price from a JSON string
price_instance = Price.from_json(json)
# print the JSON string representation of the object
print Price.to_json()

# convert the object into a dict
price_dict = price_instance.to_dict()
# create an instance of Price from a dict
price_form_dict = price.from_dict(price_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


