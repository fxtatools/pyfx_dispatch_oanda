"""GetAccountInstruments200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated

from .instrument import Instrument

from ..transport.transport_fields import TransportField
from .response_mixins import LastTransactionResponse


class GetAccountInstruments200Response(LastTransactionResponse):
    """
    GetAccountInstruments200Response
    """

    instruments: Annotated[list[Instrument], TransportField(...)]
    """The requested list of instruments.
    """


__all__ = ("GetAccountInstruments200Response",)
