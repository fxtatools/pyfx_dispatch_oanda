
"""model definition for OANDA v20 REST API (3.0.25)"""

from typing import Optional

from .instrument import Instrument

from ..transport import ApiObject, TransportField
from ..util import exporting


class GetAccountInstruments200Response(ApiObject):
    """
    GetAccountInstruments200Response
    """
    instruments: Optional[list[Instrument]] = TransportField(None)
    """The requested list of instruments.
    """
    last_transaction_id: Optional[int] = TransportField(None, alias="lastTransactionID")
    """The ID of the most recent Transaction created for the Account.
    """


__all__ = exporting(__name__, ...)
