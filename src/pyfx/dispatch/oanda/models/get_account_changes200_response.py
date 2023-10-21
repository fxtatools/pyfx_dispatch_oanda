"""GetAccountChanges200Response definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.transport_fields import TransportField

from .response_mixins import LastTransactionResponse
from .account_changes import AccountChanges
from .account_changes_state import AccountChangesState


class GetAccountChanges200Response(LastTransactionResponse):
    """
    GetAccountChanges200Response
    """

    changes: Annotated[AccountChanges, TransportField(...)]
    """The changes to the Account's Orders, Trades and Positions since the specified Transaction ID.

    Only provided if the sinceTransactionID is supplied to the poll request.
    """

    state: Annotated[AccountChangesState, TransportField(...)]
    """The Account's current price-dependent state.
    """


__all__ = ("GetAccountChanges200Response",)
