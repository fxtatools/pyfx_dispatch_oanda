
"""CreateOrder201Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from .order_cancel_transaction import OrderCancelTransaction
from .order_fill_transaction import OrderFillTransaction
from .transaction import Transaction
from .response_mixins import TransactionResponse

from ..transport.transport_fields import TransportField


class CreateOrder201Response(TransactionResponse):
    """
    CreateOrder201Response
    """

    order_create_transaction: Annotated[Optional[Transaction], TransportField(None, alias="orderCreateTransaction")]
    """The Transaction that created the Order specified by the request."""

    order_fill_transaction: Annotated[Optional[OrderFillTransaction], TransportField(None, alias="orderFillTransaction")]
    """The Transaction that filled the newly created Order.

    Only provided when the Order was immediately filled.
    """

    order_cancel_transaction: Annotated[Optional[OrderCancelTransaction], TransportField(None, alias="orderCancelTransaction")]
    """The Transaction that cancelled the newly created Order.

    Only provided when the Order was immediately cancelled.
    """

    order_reissue_transaction: Annotated[Optional[Transaction], TransportField(None, alias="orderReissueTransaction")]
    """The Transaction that reissues the Order.

    Only provided when the Order is configured to be reissued for its remaining units
    after a partial fill and the reissue was successful.
    """

    order_reissue_reject_transaction: Annotated[Optional[Transaction], TransportField(None, alias="orderReissueRejectTransaction")]
    """The Transaction that rejects the reissue of the Order.

    Only provided when the Order is configured to be reissued for its remaining units
    after a partial fill and the reissue was rejected.
    """


__all__ = ("CreateOrder201Response",)
