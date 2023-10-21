"""SetOrderClientExtensions400Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.transport_fields import TransportField
from .response_mixins import TransactionErrorResponse
from .order_client_extensions_modify_reject_transaction import OrderClientExtensionsModifyRejectTransaction


class SetOrderClientExtensions400Response(TransactionErrorResponse):
    """
    SetOrderClientExtensions400Response
    """

    order_client_extensions_modify_reject_transaction: Annotated[
        Optional[OrderClientExtensionsModifyRejectTransaction],
        TransportField(None, alias="orderClientExtensionsModifyRejectTransaction")
    ]
    """The Transaction that rejected the modification of the Client Extensions for the Order
    """


__all__ = ("SetOrderClientExtensions400Response",)
