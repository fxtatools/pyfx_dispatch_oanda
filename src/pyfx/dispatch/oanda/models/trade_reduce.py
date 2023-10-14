"""TradeReduce model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField

from .trade_id_mixin import TradeIdMixin
from .common_types import FloatValue, LotsValue, PriceValue, AccountUnits


class TradeReduce(TradeIdMixin, ApiObject):
    """
    A TradeReduce object represents a Trade for an instrument that was reduced (either partially or fully) in an Account. It is found embedded in Transactions that affect the position of an instrument in the account, specifically the OrderFill Transaction.

    Implementation Notes:
    - The field clientTradeID is supplemental to the v20 API 3.0.25 and not documented at the developer hub
    """

    units: Annotated[Optional[LotsValue], TransportField(None)]
    """
    The number of units that the Trade was reduced by
    """
    
    price: Annotated[Optional[PriceValue], TransportField(None)]
    """
    The average price that the units were closed at. This price may be clamped for guaranteed Stop Loss Orders.
    """
    
    realized_pl: Annotated[Optional[AccountUnits], TransportField(None, alias="realizedPL")]
    """
    The PL realized when reducing the Trade
    """
    
    financing: Annotated[Optional[AccountUnits], TransportField(None)]
    """
    The financing paid/collected when reducing the Trade
    """
    
    base_financing: Annotated[Optional[FloatValue], TransportField(None, alias="baseFinancing")]
    """
    The base financing paid/collected when reducing the Trade

    supplemental to the v20 API 3.0.25
    """
    
    guaranteed_execution_fee: Annotated[Optional[AccountUnits], TransportField(None, alias="guaranteedExecutionFee")]
    """
    This is the fee that is charged for closing the Trade if it has a guaranteed Stop Loss Order attached to it.
    """
    
    quote_guaranteed_execution_fee: Annotated[Optional[FloatValue], TransportField(None, alias="quoteGuaranteedExecutionFee")]
    """
    This is the fee that is charged for closing the Trade if it has a guaranteed Stop Loss Order attached to it.

    supplemental to the v20 API 3.0.25
    """
    
    half_spread_cost: Annotated[Optional[AccountUnits], TransportField(None, alias="halfSpreadCost")]
    """
    The half spread cost for the trade reduce/close. This can be a positive or negative value and is represented in the home currency of the Account.
    """

    pl_home_conversion_cost: Annotated[Optional[FloatValue], TransportField(None, alias="plHomeConversionCost")]
    """
    supplemental to the v20 API 3.0.25, not documented at the developer hub
    """

    base_financing_home_conversion_cost: Annotated[Optional[FloatValue], TransportField(None, alias="baseFinancingHomeConversionCost")]
    """
    supplemental to the v20 API 3.0.25, not documented at the developer hub
    """

    guaranteed_execution_fee_home_conversion_cost: Annotated[Optional[FloatValue], TransportField(None, alias="guaranteedExecutionFeeHomeConversionCost")]
    """
    supplemental to the v20 API 3.0.25, not documented at the developer hub
    """

    home_conversion_cost: Annotated[Optional[FloatValue], TransportField(None, alias="homeConversionCost")]
    """
    supplemental to the v20 API 3.0.25, not documented for the defining message type at the developer hub
    """


__all__ = ("TradeReduce",)
