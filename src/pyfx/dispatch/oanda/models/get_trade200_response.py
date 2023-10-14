
"""model definition for OANDA v20 REST API (3.0.25)"""




from typing import Annotated, Optional


from .trade import Trade

from ..transport import ApiObject, TransportField
from ..util import exporting



class GetTrade200Response(ApiObject):
    """
    GetTrade200Response
    """
    trade: Annotated[Optional[Trade], TransportField(None)]
    """
    The details of the requested trade
    """
    last_transaction_id: Annotated[Optional[str], TransportField(None, alias="lastTransactionID")]
    """
    The ID of the most recent Transaction created for the Account
    """


__all__ = exporting(__name__, ...)

