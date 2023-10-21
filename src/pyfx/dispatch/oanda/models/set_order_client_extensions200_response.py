"""SetOrderClientExtensions200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.transport_fields import TransportField
from .response_mixins import TransactionResponse
from .order_client_extensions_modify_transaction import OrderClientExtensionsModifyTransaction


class SetOrderClientExtensions200Response(TransactionResponse):
    """
    SetOrderClientExtensions200Response
    """

    order_client_extensions_modify_transaction: Annotated[
        Optional[OrderClientExtensionsModifyTransaction],
        TransportField(None, alias="orderClientExtensionsModifyTransaction")
    ]
    """The Transaction that modified the Client Extensions for the Order
    """

__all__ = ("SetOrderClientExtensions200Response",)
