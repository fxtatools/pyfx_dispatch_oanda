"""Mixin classes for account model classes"""

from typing import Optional

from ..transport import ApiObject, TransportField

from .common_types import AccountId, AccountUnits, FloatValue, Time
from .currency import Currency
from .guaranteed_stop_loss_order_mode import GuaranteedStopLossOrderMode
from .guaranteed_stop_loss_order_mutability import GuaranteedStopLossOrderMutability
from .guaranteed_stop_loss_order_parameters import GuaranteedStopLossOrderParameters


class AccountStateBase(ApiObject):
    """Mixin class for account state fields"""

    balance: Optional[AccountUnits] = TransportField(
        None,
    )
    """
    The current balance of the Account.
    """

    unrealized_pl: Optional[AccountUnits] = TransportField(
        None,
        alias="unrealizedPL",
    )
    """
    The total unrealized profit/loss for all Trades currently open in the Account.
    """

    nav: Optional[AccountUnits] = TransportField(
        None,
        alias="NAV",
    )
    """
    The net asset value of the Account. Equal to Account balance + unrealizedPL.
    """

    position_value: Optional[AccountUnits] = TransportField(
        None,
        alias="positionValue",
    )
    """
    The value of the Account's open positions represented in the Account's home currency.
    """

    margin_used: Optional[AccountUnits] = TransportField(
        None,
        alias="marginUsed",
    )
    """
    Margin currently used for the Account.
    """

    margin_available: Optional[AccountUnits] = TransportField(
        None,
        alias="marginAvailable",
    )
    """
    Margin available for Account currency.
    """

    margin_closeout_unrealized_pl: Optional[AccountUnits] = TransportField(
        None,
        alias="marginCloseoutUnrealizedPL",
    )
    """
    The Account's margin closeout unrealized PL.
    """

    margin_closeout_nav: Optional[AccountUnits] = TransportField(
        None,
        alias="marginCloseoutNAV",
    )
    """
    The Account's margin closeout NAV.
    """

    margin_closeout_margin_used: Optional[AccountUnits] = TransportField(
        None,
        alias="marginCloseoutMarginUsed",
    )
    """
    The Account's margin closeout margin used.
    """

    margin_closeout_percent: Optional[AccountUnits] = TransportField(
        None,
        alias="marginCloseoutPercent",
    )
    """
    The Account's margin closeout percentage. When this value is 1.0 or above the Account is in a margin closeout situation.
    """

    margin_closeout_position_value: Optional[AccountUnits] = TransportField(
        None,
        alias="marginCloseoutPositionValue",
    )
    """
    The value of the Account's open positions as used for margin closeout calculations represented in the Account's home currency.
    """

    withdrawal_limit: Optional[AccountUnits] = TransportField(
        None,
        alias="withdrawalLimit",
    )
    """
    The current WithdrawalLimit for the account which will be zero or a positive value indicating how much can be withdrawn from the account.
    """

    margin_call_margin_used: Optional[AccountUnits] = TransportField(
        None,
        alias="marginCallMarginUsed",
    )
    """
    The Account's margin call margin used.
    """

    margin_call_percent: Optional[AccountUnits] = TransportField(
        None,
        alias="marginCallPercent",
    )
    """
    The Account's margin call percentage. When this value is 1.0 or above the Account is in a margin call situation.
    """

    ##

    pl: Optional[AccountUnits] = TransportField(
        None,
    )
    """
    The total profit/loss realized over the lifetime of the Account.
    """

    resettable_pl: Optional[AccountUnits] = TransportField(
        None,
        alias="resettablePL",
    )
    """
    The total realized profit/loss for the account since it was last reset by the client.
    """

    financing: Optional[AccountUnits] = TransportField(
        None,
    )
    """
    The total amount of financing paid/collected over the lifetime of the account.
    """

    commission: Optional[AccountUnits] = TransportField(
        None,
    )
    """
    The total amount of commission paid over the lifetime of the Account.
    """

    dividend_adjustment: Optional[AccountUnits] = TransportField(
        None,
        alias="dividendAdjustment",
    )
    """
    The total amount of dividend adjustment paid over the lifetime of the Account in the Account’s home currency.
    """

    guaranteed_execution_fees: Optional[AccountUnits] = TransportField(
        None,
        alias="guaranteedExecutionFees",
    )
    """
    The total amount of fees charged over the lifetime of the Account for the execution of guaranteed Stop Loss Orders.
    """

    margin_rate: Optional[FloatValue] = TransportField(
        None,
        alias="marginRate",
    )
    """
    Client-provided margin rate override for the Account. The effective margin rate of the Account is the lesser of this value and the OANDA margin rate for the Account's division. This value is only provided if a margin rate override exists for the Account.
    """

    margin_call_enter_time: Time = TransportField(
        None,
        alias="marginCallEnterTime",
    )
    """
    The date/time when the Account entered a margin call state. Only provided if the Account is in a margin call.
    """

    margin_call_extension_count: Optional[int] = TransportField(
        None,
        alias="marginCallExtensionCount",
    )
    """
    The number of times that the Account's current margin call was extended.
    """

    last_margin_call_extension_time: Time = TransportField(
        None,
        alias="lastMarginCallExtensionTime",
    )
    """
    The date/time of the Account's last margin call extension.
    """

class AccountSummaryBase(AccountStateBase):
    """
    Mixin class for common account summary fields
    """

    id: AccountId = TransportField(
        ...,
        description="The Account's identifier")

    alias: Optional[str] = TransportField(
        None,
        description="Client-assigned alias for the Account. Only provided if the Account has an alias set")

    currency: Optional[Currency] = TransportField(
        None,
        description="The home currency of the Account")

    created_by_user_id: Optional[int] = TransportField(
        None,
        alias="createdByUserID",
        description="ID of the user that created the Account.")

    created_time: Time = TransportField(
        None,
        alias="createdTime",
        description="The date/time when the Account was created.")

    guaranteed_stop_loss_order_mode: Optional[GuaranteedStopLossOrderMode] = TransportField(
        None,
        alias="guaranteedStopLossOrderMode",
        description="The current guaranteed Stop Loss Order mode of the Account.")

    guaranteed_stop_loss_order_parameters: Optional[GuaranteedStopLossOrderParameters] = TransportField(
        None,
        alias="guaranteedStopLossOrderParameters",
        description=" The current guaranteed Stop Loss Order settings of the Account. This field will only be present if the guaranteedStopLossOrderMode is not ‘DISABLED’. [Supplemental to v20 3.25.0]")

    guaranteed_stop_loss_order_mutability: Optional[GuaranteedStopLossOrderMutability] = TransportField(
        None, deprecated=True,
        alias="guaranteedStopLossOrderMutability",
        description="The current guaranteed Stop Loss Order mutability setting of the Account. This field will only be present if the guaranteedStopLossOrderMode is not ‘DISABLED’.")

    resettable_pl_time: Time = TransportField(
        None,
        alias="resettablePLTime",
        description="The date/time that the Account's resettablePL was last reset.")

    open_trade_count: Optional[int] = TransportField(
        None,
        alias="openTradeCount",
        description="The number of Trades currently open in the Account.")

    open_position_count: Optional[int] = TransportField(
        None,
        alias="openPositionCount",
        description="The number of Positions currently open in the Account.")

    pending_order_count: Optional[int] = TransportField(
        None,
        alias="pendingOrderCount",
        description="The number of Orders currently pending in the Account.")

    hedging_enabled: Optional[bool] = TransportField(
        None,
        alias="hedgingEnabled",
        description="Flag indicating that the Account has hedging enabled.")

    last_order_fill_timestamp: Optional[Time] = TransportField(
        None,
        alias="lastOrderFillTimestamp",
        description="The date/time of the last order that was filled for this account.")


__all__ = ("AccountStateBase", "AccountSummaryBase",)
