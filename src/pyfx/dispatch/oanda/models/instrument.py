
"""model definition for OANDA v20 REST API (3.0.25)"""

from typing import Optional

from ..transport import ApiObject, TransportField

from .instrument_commission import InstrumentCommission
from .instrument_type import InstrumentType
from .guaranteed_stop_loss_order_mode import GuaranteedStopLossOrderMode
from .guaranteed_stop_loss_order_level_restriction import GuaranteedStopLossOrderLevelRestriction
from .instrument_financing import InstrumentFinancing
from .tag import Tag

from .common_types import PriceValue, LotsValue, FloatValue

from .currency import Currency


class Instrument(ApiObject):
    """
    Full specification of an Instrument.

    updated supplemental to the fxTrade v20 API version 3.0.25
    """

    name: str = TransportField(...)
    """
    The name of the Instrument
    """

    type: InstrumentType = TransportField(...)
    """
    The type of the Instrument
    """

    display_name: str = TransportField(..., alias="displayName")
    """
    The display name of the Instrument
    """

    pip_location: int = TransportField(..., alias="pipLocation")
    """
    The location of the \"pip\" for this instrument. The decimal position of the pip in this Instrument's price can be found at `10 ^ pipLocation` (e.g. `-4` pipLocation results in a decimal pip position of `10 ^ -4 = 0.0001`).
    """

    display_precision: int = TransportField(..., alias="displayPrecision")
    """
    The number of decimal places that should be used to display prices for this instrument. (e.g. a displayPrecision of 5 would result in a price of \"1\" being displayed as \"1.00000\")
    """

    trade_units_precision: Optional[int] = TransportField(None, alias="tradeUnitsPrecision")
    """
    The amount of decimal places that may be provided when specifying the number of units traded for this instrument.
    """

    minimum_trade_size: Optional[LotsValue] = TransportField(None, alias="minimumTradeSize")
    """
    The smallest number of units allowed to be traded for this instrument.
    """

    maximum_trailing_stop_distance: Optional[PriceValue] = TransportField(None, alias="maximumTrailingStopDistance")
    """
    The maximum trailing stop distance allowed for a trailing stop loss created for this instrument. Specified in price units.
    """

    minimum_trailing_stop_distance: Optional[PriceValue] = TransportField(None, alias="minimumTrailingStopDistance")
    """
    The minimum trailing stop distance allowed for a trailing stop loss created for this instrument. Specified in price units.
    """

    maximum_position_size: Optional[LotsValue] = TransportField(None, alias="maximumPositionSize")
    """
    The maximum position size allowed for this instrument. Specified in units.
    """

    maximum_order_units: Optional[LotsValue] = TransportField(None, alias="maximumOrderUnits")
    """
    The maximum units allowed for an Order placed for this instrument. Specified in units.
    """

    margin_rate: Optional[FloatValue] = TransportField(None, alias="marginRate")
    """
    The margin rate for this instrument.
    """

    commission: Optional[InstrumentCommission] = TransportField(None)
    """
    The commission structure for this instrument.
    """

    #
    # the following fields are supplemental to OANDA's v20.json 3.0.25
    #

    guaranteed_stop_loss_order_mode: Optional[GuaranteedStopLossOrderMode] = TransportField(
        None, alias="guaranteedStopLossOrderMode")
    """
    The current Guaranteed Stop Loss Order mode of the Account for this Instrument.
    """

    guaranteed_stop_loss_order_execution_premium: Optional[PriceValue] = TransportField(
        None, alias="guaranteedStopLossOrderExecutionPremium")
    """
    The amount that is charged to the account if a guaranteed Stop Loss Order is triggered and filled. The value is in price units and is charged for each unit of the Trade. This field will only be present if the Account’s guaranteedStopLossOrderMode for this Instrument is not ‘DISABLED’.
    """

    guaranteed_stop_loss_order_level_restriction: Optional[GuaranteedStopLossOrderLevelRestriction] = TransportField(
        None, alias="guaranteedStopLossOrderLevelRestriction")
    """
    The guaranteed Stop Loss Order level restriction for this instrument. This field will only be present if the Account’s guaranteedStopLossOrderMode for this Instrument is not ‘DISABLED’.
    """

    financing: Optional[InstrumentFinancing] = TransportField(None)
    """
    Financing data for this instrument
    """

    tags: Optional[list[Tag]] = TransportField(None)
    """
    The tags associated with this instrument.
    """


__all__ = ("Instrument",)
