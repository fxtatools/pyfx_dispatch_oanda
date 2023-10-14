
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Annotated, Optional


from .trade_client_extensions_modify_transaction import TradeClientExtensionsModifyTransaction


from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting


class SetTradeClientExtensions200Response(ApiObject):
    """
    SetTradeClientExtensions200Response
    """
    trade_client_extensions_modify_transaction: Annotated[Optional[TradeClientExtensionsModifyTransaction], TransportField(None, alias="tradeClientExtensionsModifyTransaction")]
    related_transaction_ids: Annotated[Optional[list[str]], TransportField(None, alias="relatedTransactionIDs")]
    """
    The IDs of all Transactions that were created while satisfying the request.
    """
    last_transaction_id: Annotated[Optional[str], TransportField(None, alias="lastTransactionID")]
    """
    The ID of the most recent Transaction created for the Account
    """


__all__ = exporting(__name__, ...)
