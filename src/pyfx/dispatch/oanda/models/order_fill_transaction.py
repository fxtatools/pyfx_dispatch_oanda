"""OrderFillTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal, Optional

from .client_price import ClientPrice
from .trade_open import TradeOpen
from .trade_reduce import TradeReduce

from ..transport.transport_fields import TransportField

from .transaction_mixins import InstrumentTxn
from .transaction_type import TransactionType
from .order_identifier import OrderIdentifier
from .order_fill_reason import OrderFillReason
from .common_types import PriceValue, LotsValue, AccountUnits, FloatValue
from .home_conversion_factors import HomeConversionFactors


class OrderFillTransaction(InstrumentTxn, OrderIdentifier):
    """
    An OrderFillTransaction represents the filling of an Order in the client's Account.
    """

    type: Annotated[Literal[TransactionType.ORDER_FILL], TransportField(TransactionType.ORDER_FILL)] = TransactionType.ORDER_FILL
    """
    The Type of the Transaction. Always set to \"ORDER_FILL\" for an OrderFillTransaction.
    """

    requested_units: Annotated[Optional[LotsValue], TransportField(None, alias="requestedUnits")]
    ## FIXME clarify with OANDA
    """
    The number of units requested by the OrderFill (assumed meaning)

    This field is supplemental to the fxTrade v20 API 3.0.25 and not documented at the developer hub
    """

    gain_quote_home_conversion_factor: Annotated[Optional[FloatValue], TransportField(None, alias="gainQuoteHomeConversionFactor", deprecated=True)]
    """
    This is the conversion factor in effect for the Account at the time of the OrderFill for converting any gains realized in Instrument quote units into units of the Account's home currency.
    """

    loss_quote_home_conversion_factor: Annotated[Optional[FloatValue], TransportField(None, alias="lossQuoteHomeConversionFactor", deprecated=True)]
    """
    This is the conversion factor in effect for the Account at the time of the OrderFill for converting any losses realized in Instrument quote units into units of the Account's home currency.
    """

    home_conversion_factors: Annotated[Optional[HomeConversionFactors], TransportField(None, alias="homeConversionFactors")]
    """
    The HomeConversionFactors in effect at the time of the OrderFill.
    """

    price: Annotated[Optional[PriceValue], TransportField(None, deprecated=True)]
    """
    This field is now deprecated and should no longer be used. The individual tradesClosed, tradeReduced and tradeOpened fields contain the exact/official price each unit was filled at.
    """

    full_vwap: Annotated[Optional[PriceValue], TransportField(None, alias="fullVWAP")]
    """
    The price that all of the units of the OrderFill should have been filled at, in the absence of guaranteed price execution. This factors in the Account's current ClientPrice, used liquidity and the units of the OrderFill only. If no Trades were closed with their price clamped for guaranteed stop loss enforcement, then this value will match the price fields of each Trade opened, closed, and reduced, and they will all be the exact same.
    """

    full_price: Annotated[Optional[ClientPrice], TransportField(None, alias="fullPrice")]
    """
    The price in effect for the account at the time of the Order fill.
    """

    reason: Annotated[Optional[OrderFillReason], TransportField(None)]
    """
    The reason that an Order was filled
    """

    pl: Annotated[Optional[AccountUnits], TransportField(None)]
    """
    The profit or loss incurred when the Order was filled.
    """

    quote_pl: Annotated[Optional[FloatValue], TransportField(None, alias="quotePL")]
    """
    The profit or loss incurred when the Order was filled, in the Instrument's quote currency.

    supplemental to the fxTrade v20 API 3.0.25
    """

    financing: Annotated[Optional[AccountUnits], TransportField(None)]
    """
    The financing paid or collected when the Order was filled.
    """

    base_financing: Annotated[Optional[FloatValue], TransportField(None, alias="baseFinancing")]
    """
    The financing paid or collected when the Order was filled, in the Instrument's base currency.
    """

    quote_financing: Annotated[Optional[FloatValue], TransportField(None, alias="quoteFinancing")]
    """
    The financing paid or collected when the Order was filled, in the Instrument's quote currency.
    """

    commission: Annotated[Optional[AccountUnits], TransportField(None)]
    """
    The commission charged in the Account's home currency as a result of filling the Order. The commission is always represented as a positive quantity of the Account's home currency, however it reduces the balance in the Account.
    """

    guaranteed_execution_fee: Annotated[Optional[AccountUnits], TransportField(None, alias="guaranteedExecutionFee")]
    """
    The total guaranteed execution fees charged for all Trades opened, closed or reduced with guaranteed Stop Loss Orders.
    """

    quote_guaranteed_execution_fee: Annotated[Optional[FloatValue], TransportField(None, alias="quoteGuaranteedExecutionFee")]
    """
    The total guaranteed execution fees charged for all Trades opened, closed
    or reduced with guaranteed Stop Loss Orders, expressed in the
    Instrument's quote currency.

    supplemental to the fxTrade v20 API 3.0.25
    """

    account_balance: Annotated[Optional[AccountUnits], TransportField(None, alias="accountBalance")]
    """
    The Account's balance after the Order was filled.
    """

    trade_opened: Annotated[Optional[TradeOpen], TransportField(None, alias="tradeOpened")]
    """
    The Trade that was opened when the Order was filled (only provided if filling the Order resulted in a new Trade).
    """

    trades_closed: Annotated[Optional[list[TradeReduce]], TransportField(None, alias="tradesClosed")]
    """
    The Trades that were closed when the Order was filled (only provided if filling the Order resulted in a closing open Trades).
    """

    trade_reduced: Annotated[Optional[TradeReduce], TransportField(None, alias="tradeReduced")]
    """
    The Trade that was reduced when the Order was filled (only provided if
    filling the Order resulted in reducing an open Trade).
    """

    half_spread_cost: Annotated[Optional[AccountUnits], TransportField(None, alias="halfSpreadCost")]
    """
    The half spread cost for the OrderFill, which is the sum of the halfSpreadCost values in the tradeOpened, tradesClosed and tradeReduced fields. This can be a positive or negative value and is represented in the home currency of the Account.
    """

    pl_home_conversion_cost: Annotated[Optional[FloatValue], TransportField(None, alias="plHomeConversionCost")]
    """
    This field is supplemental to the fxTrade v20 API 3.0.25 and not documented at the developer hub
    """

    base_financing_home_conversion_cost: Annotated[Optional[FloatValue], TransportField(None, alias="baseFinancingHomeConversionCost")]
    """
    This field is supplemental to the fxTrade v20 API 3.0.25 and not documented at the developer hub
    """

    guaranteed_execution_feed_home_conversion_cost: Annotated[Optional[FloatValue], TransportField(None, alias="guaranteedExecutionFeeHomeConversionCost")]
    """
    This field is supplemental to the fxTrade v20 API 3.0.25 and not documented at the developer hub
    """

    home_conversion_cost: Annotated[Optional[FloatValue], TransportField(None, alias="homeConversionCost")]
    """
    This field is supplemental to the fxTrade v20 API 3.0.25 and not documented at the developer hub
    """


__all__ = ("OrderFillTransaction",)
