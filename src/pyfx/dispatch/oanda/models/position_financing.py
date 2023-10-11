
"""PositionFinancing model definition for OANDA v20 REST API (3.0.25)"""

from typing import Optional

from ..transport import ApiObject, TransportField
from .common_types import InstrumentName, AccountUnits, FloatValue
from .open_trade_financing import OpenTradeFinancing
from .home_conversion_factors import HomeConversionFactors
from .account_financing_mode import AccountFinancingMode


class PositionFinancing(ApiObject):
    """
    OpenTradeFinancing is used to pay/collect daily financing charge for a Position within an Account
    """

    instrument: Optional[InstrumentName] = TransportField(None)
    """
    The instrument of the Position that financing is being paid/collected for.
    """

    financing: Optional[AccountUnits] = TransportField(None)
    """
    The amount of financing paid/collected for the Position.
    """

    open_trade_financings: Optional[list[OpenTradeFinancing]] = TransportField(None, alias="openTradeFinancings")
    """
    The financing paid/collecte for each open Trade within the Position.
    """

    base_financing: Optional[FloatValue] = TransportField(None, alias="baseFinancing")
    """
    The amount of base financing paid/collected for the Position.

    supplemental to the fxTrade v20 API 3.0.25
    """

    quote_financing: Optional[FloatValue] = TransportField(None, alias="quoteFinancing")
    """
    The amount of quote financing paid/collected for the Position.

    supplemental to the fxTrade v20 API 3.0.25
    """

    home_conversion_factors: Optional[HomeConversionFactors] = TransportField(None, alias="homeConversionFactors")
    """
    The HomeConversionFactors in effect for the Position’s Instrument at the time of the DailyFinancing.

    supplemental to the fxTrade v20 API 3.0.25
    """

    account_financing_mode: Optional[AccountFinancingMode] = TransportField(None, alias="accountFinancingMode")
    """
    The account financing mode at the time of the daily financing.

    supplemental to the fxTrade v20 API 3.0.25
    """


__all__ = ("PositionFinancing",)
