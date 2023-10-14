
"""model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal

from ..transport.transport_fields import TransportField

from .order_client_extensions_modify_transaction import OrderClientExtensionsModifyTransaction
from .transaction_mixins import RejectTxn
from .transaction_type import TransactionType


class OrderClientExtensionsModifyRejectTransaction(RejectTxn, OrderClientExtensionsModifyTransaction):
    """
    A OrderClientExtensionsModifyRejectTransaction represents the rejection of the modification of an Order's Client Extensions.
    """

    type: Annotated[Literal[TransactionType.ORDER_CLIENT_EXTENSIONS_MODIFY_REJECT], TransportField(TransactionType.ORDER_CLIENT_EXTENSIONS_MODIFY_REJECT)] = TransactionType.ORDER_CLIENT_EXTENSIONS_MODIFY_REJECT
    """The Type of the Transaction. Always set to \"ORDER_CLIENT_EXTENSIONS_MODIFY_REJECT\" for a OrderClientExtensionsModifyRejectTransaction.
    """


__all__ = ("OrderClientExtensionsModifyRejectTransaction",)
