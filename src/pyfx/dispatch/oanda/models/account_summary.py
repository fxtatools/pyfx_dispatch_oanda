
"""AccountSummary model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.transport_fields import TransportField

from .account_mixins import AccountSummaryBase


class AccountSummary(AccountSummaryBase):
    """
    A summary representation of a client's Account. The AccountSummary does not provide to full specification of pending Orders, open Trades and Positions.
    """

    last_transaction_id: Annotated[Optional[str], TransportField(None, alias="lastTransactionID")]
    """The ID of the last Transaction created for the Account.
    """


__all__ = ("AccountSummary",)
