
"""TradeClientExtensionsModifyRejectTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal

from ..transport import TransportField

from .trade_client_extensions_modify_transaction import TradeClientExtensionsModifyTransaction
from .transaction_mixins import RejectTxn
from .transaction_type import TransactionType


class TradeClientExtensionsModifyRejectTransaction(RejectTxn, TradeClientExtensionsModifyTransaction):
    """
    A TradeClientExtensionsModifyRejectTransaction represents the rejection of the modification of a Trade's Client Extensions.
    """
    type: Literal[TransactionType.TRADE_CLIENT_EXTENSIONS_MODIFY_REJECT] = TransportField(TransactionType.TRADE_CLIENT_EXTENSIONS_MODIFY_REJECT)
    """
    The Type of the Transaction. Always set to \"TRADE_CLIENT_EXTENSIONS_MODIFY_REJECT\" for a TradeClientExtensionsModifyRejectTransaction.
    """


__all__ = ("TradeClientExtensionsModifyRejectTransaction",)
