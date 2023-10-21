"""GuaranteedStopLossOrderRejectTransaction model definition for OANDA v20 REST API, supplemental to 3.0.25"""

from typing import Annotated, Literal

from ..transport.transport_fields import TransportField
from .transaction_mixins import RejectTxn
from .guaranteed_stop_loss_order_transaction import GuaranteedStopLossOrderTransaction
from .transaction_type import TransactionType


class GuaranteedStopLossOrderRejectTransaction (RejectTxn, GuaranteedStopLossOrderTransaction):
    """A GuaranteedStopLossOrderRejectTransaction represents the rejection of the creation of a GuaranteedStopLoss Order.

    supplemental to v20 API 3.0.25
    """

    type: Annotated[ # type: ignore
        Literal[TransactionType.GUARANTEED_STOP_LOSS_ORDER_REJECT],
        TransportField(...)
    ] = TransactionType.GUARANTEED_STOP_LOSS_ORDER_REJECT # type: ignore
    """The Type of the Transaction. Always set to "GUARANTEED_STOP_LOSS_ORDER_REJECT" in a StopLossOrderRejectTransaction.
    """


__all__ = ("GuaranteedStopLossOrderRejectTransaction",)
