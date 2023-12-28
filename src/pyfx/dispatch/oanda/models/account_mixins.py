"""Mixin classes for account model classes"""

from abc import ABC
from typing import Annotated, Optional

from ..transport.account_id import AccountId

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField

from .common_types import AccountUnits, FloatValue, Time
from .currency import Currency
from .guaranteed_stop_loss_order_mode import GuaranteedStopLossOrderMode
from .guaranteed_stop_loss_order_mutability import GuaranteedStopLossOrderMutability
from .guaranteed_stop_loss_order_parameters import GuaranteedStopLossOrderParameters


class AccountStateBase(ApiObject, ABC):
    """Mixin class for commmon account state fields"""

    balance: Annotated[Optional[AccountUnits], TransportField(None)]
    """
    The current balance of the Account.
    """

    unrealized_pl: Annotated[Optional[AccountUnits], TransportField(None, alias="unrealizedPL")]
    """
    The total unrealized profit/loss for all Trades currently open in the Account.
    """

    nav: Annotated[Optional[AccountUnits], TransportField(None, alias="NAV")]
    """
    The net asset value of the Account. Equal to Account balance + unrealizedPL.
    """

    position_value: Annotated[Optional[AccountUnits], TransportField(None, alias="positionValue")]
    """
    The value of the Account's open positions represented in the Account's home currency.
    """

    margin_used: Annotated[Optional[AccountUnits], TransportField(None, alias="marginUsed")]
    """
    Margin currently used for the Account.
    """

    margin_available: Annotated[Optional[AccountUnits], TransportField(None, alias="marginAvailable")]
    """
    Margin available for Account currency.
    """

    margin_closeout_unrealized_pl: Annotated[Optional[AccountUnits], TransportField(None, alias="marginCloseoutUnrealizedPL")]
    """
    The Account's margin closeout unrealized PL.
    """

    margin_closeout_nav: Annotated[Optional[AccountUnits], TransportField(None, alias="marginCloseoutNAV")]
    """
    The Account's margin closeout NAV.
    """

    margin_closeout_margin_used: Annotated[Optional[AccountUnits], TransportField(None, alias="marginCloseoutMarginUsed")]
    """
    The Account's margin closeout margin used.
    """

    margin_closeout_percent: Annotated[Optional[AccountUnits], TransportField(None, alias="marginCloseoutPercent")]
    """
    The Account's margin closeout percentage.

    When this value is 1.0 or above the Account is in a margin closeout situation.
    """

    margin_closeout_position_value: Annotated[Optional[AccountUnits], TransportField(None, alias="marginCloseoutPositionValue")]
    """
    The value of the Account's open positions as used for margin closeout calculations represented in the Account's home currency.
    """

    withdrawal_limit: Annotated[Optional[AccountUnits], TransportField(None, alias="withdrawalLimit")]
    """
    The current WithdrawalLimit for the account which will be zero or a positive value indicating how much can be withdrawn from the account.
    """

    margin_call_margin_used: Annotated[Optional[AccountUnits], TransportField(None, alias="marginCallMarginUsed")]
    """
    The Account's margin call margin used.
    """

    margin_call_percent: Annotated[Optional[AccountUnits], TransportField(None, alias="marginCallPercent")]
    """
    The Account's margin call percentage. When this value is 1.0 or above the Account is in a margin call situation.
    """

    ##

    pl: Annotated[Optional[AccountUnits], TransportField(None)]
    """
    The total profit/loss realized over the lifetime of the Account.
    """

    resettable_pl: Annotated[Optional[AccountUnits], TransportField(None, alias="resettablePL")]
    """
    The total realized profit/loss for the account since it was last reset by the client.
    """

    financing: Annotated[Optional[AccountUnits], TransportField(None)]
    """
    The total amount of financing paid/collected over the lifetime of the account.
    """

    commission: Annotated[Optional[AccountUnits], TransportField(None)]
    """
    The total amount of commission paid over the lifetime of the Account.
    """

    dividend_adjustment: Annotated[Optional[AccountUnits], TransportField(None, alias="dividendAdjustment")]
    """
    The total amount of dividend adjustment paid over the lifetime of the Account in the Account's home currency.
    """

    guaranteed_execution_fees: Annotated[Optional[AccountUnits], TransportField(None, alias="guaranteedExecutionFees")]
    """
    The total amount of fees charged over the lifetime of the Account for the execution of guaranteed Stop Loss Orders.
    """

    margin_rate: Annotated[Optional[FloatValue], TransportField(None, alias="marginRate")]
    """
    Client-provided margin rate override for the Account.

    The effective margin rate of the Account is the lesser of this value and the OANDA margin rate for the Account's division.

    This value is only provided if a margin rate override exists for the Account.
    """

    margin_call_enter_time: Annotated[Optional[Time], TransportField(None, alias="marginCallEnterTime")]
    """
    The date/time when the Account entered a margin call state. Only provided if the Account is in a margin call.
    """

    margin_call_extension_count: Annotated[Optional[int], TransportField(None, alias="marginCallExtensionCount")]
    """
    The number of times that the Account's current margin call was extended.
    """

    last_margin_call_extension_time: Annotated[Optional[Time], TransportField(None, alias="lastMarginCallExtensionTime")]
    """
    The date/time of the Account's last margin call extension.
    """

class AccountSummaryBase(AccountStateBase, ABC):
    """
    Mixin class for common account summary fields
    """

    id: Annotated[AccountId, TransportField(...)]
    "The Account's identifier"

    alias: Annotated[Optional[str], TransportField(None)]
    "Client-assigned alias for the Account. Only provided if the Account has an alias set"

    currency: Annotated[Currency, TransportField(...)]
    "The home currency of the Account"

    created_by_user_id: Annotated[Optional[int], TransportField(None, alias="createdByUserID")]
    "ID of the user that created the Account."

    created_time: Annotated[Time, TransportField(..., alias="createdTime")]
    "The date/time when the Account was created."

    guaranteed_stop_loss_order_mode: Annotated[Optional[GuaranteedStopLossOrderMode], TransportField(
        None, alias="guaranteedStopLossOrderMode")]
    "The current guaranteed Stop Loss Order mode of the Account."

    guaranteed_stop_loss_order_parameters: Annotated[Optional[GuaranteedStopLossOrderParameters], TransportField(
        None, alias="guaranteedStopLossOrderParameters")]
    """The current guaranteed Stop Loss Order settings of the Account.

    This field will only be present if the guaranteedStopLossOrderMode is not 'DISABLED'.

    [Supplemental to v20 3.25.0]
    """

    guaranteed_stop_loss_order_mutability: Annotated[Optional[GuaranteedStopLossOrderMutability], TransportField(
        None, deprecated=True, alias="guaranteedStopLossOrderMutability")]
    """The current guaranteed Stop Loss Order mutability setting of the Account.

    This field will only be present if the guaranteedStopLossOrderMode is not 'DISABLED'.
    """

    resettable_pl_time: Annotated[Time, TransportField(0, alias="resettablePLTime")]
    """The date/time that the Account's resettablePL was last reset.

    ### Implentation Note

    `resettable_pl_time` represents a nullable datetime value. For server responses encoding
    the value as "0", the value will be processed as `pandas.NaT`
    """

    open_trade_count: Annotated[Optional[int], TransportField(None, alias="openTradeCount")]
    "The number of Trades currently open in the Account."

    open_position_count: Annotated[Optional[int], TransportField(None, alias="openPositionCount")]
    "The number of Positions currently open in the Account."

    pending_order_count: Annotated[Optional[int], TransportField(None, alias="pendingOrderCount")]
    "The number of Orders currently pending in the Account."

    hedging_enabled: Annotated[Optional[bool], TransportField(None, alias="hedgingEnabled")]
    "Flag indicating that the Account has hedging enabled."

    last_order_fill_timestamp: Annotated[Optional[Time], TransportField(None, alias="lastOrderFillTimestamp")]
    "The date/time of the last order that was filled for this account."


__all__ = ("AccountStateBase", "AccountSummaryBase")
