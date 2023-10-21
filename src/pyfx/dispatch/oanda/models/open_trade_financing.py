"""OpenTradeFinancing model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from .common_types import TradeId, AccountUnits, FloatValue


class OpenTradeFinancing(ApiObject):
    """
    OpenTradeFinancing is used to pay/collect daily financing charge for an open Trade within an Account
    """

    trade_id: Annotated[TradeId, TransportField(..., alias="tradeID")]
    """
    The ID of the Trade that financing is being paid/collected for.
    """

    financing: Annotated[AccountUnits, TransportField(...)]
    """
    The amount of financing paid/collected for the Trade.
    """

    base_financing: Annotated[FloatValue, TransportField(..., alias="baseFinancing")]
    """The amount of financing paid/collected in the Instrument's base currency for the Trade.

    supplemental to the fxTrade v20 API 3.0.25
    """

    quote_financing: Annotated[Optional[FloatValue], TransportField(..., alias="quoteFinancing")]
    """The amount of financing paid/collected in the Instrument's quote currency for the Trade.

    supplemental to the fxTrade v20 API 3.0.25
    """

    financing_rate: Annotated[Optional[FloatValue], TransportField(None, alias="financingRate")]
    """The financing rate in effect for the instrument used to calculate the the amount of financing
    paid/collected for the Trade.

    This field will only be set if the AccountFinancingMode at the time of the daily  financing is
    `DAILY_INSTRUMENT` or `SECOND_BY_SECOND_INSTRUMENT`. The value is in decimal rather than percentage
    points, e.g. 5% is represented as 0.05.

    supplemental to the fxTrade v20 API 3.0.25
    """


__all__ = ("OpenTradeFinancing",)
