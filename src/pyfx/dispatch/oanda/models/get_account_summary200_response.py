"""GetAccountSummary200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from .account_summary import AccountSummary

from ..transport.transport_fields import TransportField
from .response_mixins import LastTransactionResponse


class GetAccountSummary200Response(LastTransactionResponse):
    """
    GetAccountSummary200Response
    """

    account: Annotated[AccountSummary, TransportField(...)]
    """The summary of the requested Account.
    """


__all__ = ("GetAccountSummary200Response",)
