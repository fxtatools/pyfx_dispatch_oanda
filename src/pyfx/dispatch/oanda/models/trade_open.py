"""TradeOpen model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from .client_extensions import ClientExtensions

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from .common_types import TradeId, LotsValue, PriceValue, FloatValue, AccountUnits


class TradeOpen(ApiObject):
    """
    A TradeOpen object represents a Trade for an instrument that was opened in an Account. It is found embedded in Transactions that affect the position of an instrument in the Account, specifically the OrderFill Transaction.
    """

    trade_id: Annotated[Optional[TradeId], TransportField(None, alias="tradeID")]
    """
    The ID of the Trade that was opened
    """

    units: Annotated[Optional[LotsValue], TransportField(None)]
    """
    The number of units opened by the Trade
    """

    price: Annotated[Optional[PriceValue], TransportField(None)]
    """
    The average price that the units were opened at.
    """

    guaranteed_execution_fee: Annotated[Optional[AccountUnits], TransportField(None, alias="guaranteedExecutionFee")]
    """
    This is the fee charged for opening the trade if it has a guaranteed Stop Loss Order attached to it.
    """

    client_extensions: Annotated[Optional[ClientExtensions], TransportField(None, alias="clientExtensions")]
    """
    The client extensions for the newly opened Trade
    """

    half_spread_cost: Annotated[Optional[AccountUnits], TransportField(None, alias="halfSpreadCost")]
    """
    The half spread cost for the trade open. This can be a positive or negative value and is represented in the home currency of the Account.
    """

    initial_margin_required: Annotated[Optional[AccountUnits], TransportField(None, alias="initialMarginRequired")]
    """
    The margin required at the time the Trade was created. Note, this is the 'pure' margin required, it is not the 'effective' margin used that factors in the trade risk if a GSLO is attached to the trade.
    """

    guaranteed_execution_fee_home_conversion_cost: Annotated[Optional[FloatValue], TransportField(None, alias="guaranteedExecutionFeeHomeConversionCost")]
    """
    This is the fee charged for opening the trade if it has a guaranteed Stop Loss Order attached to it.
    
    supplemental to v20 API 3.0.25
    """

    quote_guaranteed_execution_fee: Annotated[Optional[FloatValue], TransportField(None, alias="quoteGuaranteedExecutionFee")]
    """
    This is the fee charged for opening the trade if it has a guaranteed Stop Loss Order attached to it, expressed in the Instrument’s quote currency.

    supplemental to v20 API 3.0.25
    """


__all__ = ("TradeOpen",)
