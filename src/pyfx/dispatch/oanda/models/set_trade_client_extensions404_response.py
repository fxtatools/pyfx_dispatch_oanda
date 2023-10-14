
"""model definition for OANDA v20 REST API (3.0.25)"""




from typing import Annotated, Optional


from .trade_client_extensions_modify_reject_transaction import TradeClientExtensionsModifyRejectTransaction


from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting



class SetTradeClientExtensions404Response(ApiObject):
    """
    SetTradeClientExtensions404Response
    """
    trade_client_extensions_modify_reject_transaction: Annotated[Optional[TradeClientExtensionsModifyRejectTransaction], TransportField(None, alias="tradeClientExtensionsModifyRejectTransaction")]
    last_transaction_id: Annotated[Optional[str], TransportField(None, alias="lastTransactionID")]
    """
    The ID of the most recent Transaction created for the Account. Only present if the Account exists.
    """
    related_transaction_ids: Annotated[Optional[list[str]], TransportField(None, alias="relatedTransactionIDs")]
    """
    The IDs of all Transactions that were created while satisfying the request. Only present if the Account exists.
    """
    error_code: Annotated[Optional[str], TransportField(None, alias="errorCode")]
    """
    The code of the error that has occurred. This field may not be returned for some errors.
    """
    error_message: Annotated[Optional[str], TransportField(None, alias="errorMessage")]
    """
    The human-readable description of the error that has occurred.
    """


__all__ = exporting(__name__, ...)

