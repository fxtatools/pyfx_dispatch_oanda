
"""model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from .account_summary import AccountSummary

from ..transport import ApiObject, TransportField
from ..util import exporting


class GetAccountSummary200Response(ApiObject):
    """
    GetAccountSummary200Response
    """
    account: Annotated[Optional[AccountSummary], TransportField(None)]
    """The summary of the requested Account.
    """
    last_transaction_id: Annotated[Optional[str], TransportField(None, alias="lastTransactionID")]
    """The ID of the most recent Transaction created for the Account.
    """


__all__ = exporting(__name__, ...)
