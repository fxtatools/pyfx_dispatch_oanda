
"""model definition for OANDA v20 REST API (3.0.25)"""




from typing import Optional


from .account_changes import AccountChanges
from .account_changes_state import AccountChangesState

from ..transport import ApiObject, TransportField
from ..util import exporting



class GetAccountChanges200Response(ApiObject):
    """
    GetAccountChanges200Response
    """
    changes: Optional[AccountChanges] = TransportField(None)
    """The changes to the Account’s Orders, Trades and Positions since the specified Transaction ID. Only provided if the sinceTransactionID is supplied to the poll request.
    """
    state: Optional[AccountChangesState] = TransportField(None)
    """The Account’s current price-dependent state.
    """
    last_transaction_id: Optional[str] = TransportField(None, alias="lastTransactionID")
    """The ID of the last Transaction created for the Account.  This Transaction ID should be used for future poll requests, as the client has already observed all changes up to and including it.
    """


__all__ = exporting(__name__, ...)

