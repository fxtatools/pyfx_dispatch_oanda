# ClientPrice

The specification of an Account-specific Price.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The string \&quot;PRICE\&quot;. Used to identify the a Price object when found in a stream. | [optional] 
**instrument** | **str** | The Price&#39;s Instrument. | [optional] 
**time** | **str** | The date/time when the Price was created | [optional] 
**status** | **str** | The status of the Price. | [optional] 
**tradeable** | **bool** | Flag indicating if the Price is tradeable or not | [optional] 
**bids** | [**List[PriceBucket]**](PriceBucket.md) | The list of prices and liquidity available on the Instrument&#39;s bid side. It is possible for this list to be empty if there is no bid liquidity currently available for the Instrument in the Account. | [optional] 
**asks** | [**List[PriceBucket]**](PriceBucket.md) | The list of prices and liquidity available on the Instrument&#39;s ask side. It is possible for this list to be empty if there is no ask liquidity currently available for the Instrument in the Account. | [optional] 
**closeout_bid** | **str** | The closeout bid Price. This Price is used when a bid is required to closeout a Position (margin closeout or manual) yet there is no bid liquidity. The closeout bid is never used to open a new position. | [optional] 
**closeout_ask** | **str** | The closeout ask Price. This Price is used when a ask is required to closeout a Position (margin closeout or manual) yet there is no ask liquidity. The closeout ask is never used to open a new position. | [optional] 
**quote_home_conversion_factors** | [**QuoteHomeConversionFactors**](QuoteHomeConversionFactors.md) |  | [optional] 
**units_available** | [**UnitsAvailable**](UnitsAvailable.md) |  | [optional] 

## Example

```python
from pyfx.dispatch.oanda.models.client_price import ClientPrice

# TODO update the JSON string below
json = "{}"
# create an instance of ClientPrice from a JSON string
client_price_instance = ClientPrice.from_json(json)
# print the JSON string representation of the object
print ClientPrice.to_json()

# convert the object into a dict
client_price_dict = client_price_instance.to_dict()
# create an instance of ClientPrice from a dict
client_price_form_dict = client_price.from_dict(client_price_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


