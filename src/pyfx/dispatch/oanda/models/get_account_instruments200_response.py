
"""model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from .instrument import Instrument

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting


class GetAccountInstruments200Response(ApiObject):
    """
    GetAccountInstruments200Response
    """
    instruments: Annotated[Optional[list[Instrument]], TransportField(None)]
    """The requested list of instruments.
    """
    last_transaction_id: Annotated[Optional[int], TransportField(None, alias="lastTransactionID")]
    """The ID of the most recent Transaction created for the Account.
    """


__all__ = exporting(__name__, ...)
