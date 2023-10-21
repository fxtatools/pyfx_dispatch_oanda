"""ReplaceOrder201Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from .order_cancel_transaction import OrderCancelTransaction
from .order_fill_transaction import OrderFillTransaction
from .transaction import Transaction

from ..transport.transport_fields import TransportField

from .response_mixins import TransactionResponse


class ReplaceOrder201Response(TransactionResponse):
    """
    ReplaceOrder201Response
    """

    order_cancel_transaction: Annotated[Optional[OrderCancelTransaction], TransportField(None, alias="orderCancelTransaction")]
    """The Transaction that cancelled the Order to be replaced.
    """

    order_create_transaction: Annotated[Optional[Transaction], TransportField(None, alias="orderCreateTransaction")]
    """The Transaction that created the replacing Order as requested.
    """

    order_fill_transaction: Annotated[Optional[OrderFillTransaction], TransportField(None, alias="orderFillTransaction")]
    """ The Transaction that filled the replacing Order.

    This is only provided when the replacing Order was immediately filled.
    """

    order_reissue_transaction: Annotated[Optional[Transaction], TransportField(None, alias="orderReissueTransaction")]
    """The Transaction that reissues the replacing Order.

    Only provided when the replacing Order was partially filled immediately and is configured to be reissued for its remaining units.
    """

    order_reissue_reject_transaction: Annotated[Optional[Transaction], TransportField(None, alias="orderReissueRejectTransaction")]
    """The Transaction that rejects the reissue of the Order.

    Only provided when the replacing Order was partially filled immediately and was configured to be reissued,
    however the reissue was rejected.
    """

    replacing_order_cancel_transaction: Annotated[Optional[OrderCancelTransaction], TransportField(None, alias="replacingOrderCancelTransaction")]
    """The Transaction that cancelled the replacing Order.

    Only provided when the replacing Order was immediately cancelled.
    """


__all__ = ("ReplaceOrder201Response",)
