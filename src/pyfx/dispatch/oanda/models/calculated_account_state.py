
"""CalculatedAccountState model definition for OANDA v20 REST API (3.0.25)"""

from typing import Optional

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting

from .account_mixins import AccountSummaryBase


class CalculatedAccountState(AccountSummaryBase):
    """
    The dynamically calculated state of a client's Account.
    """
    ## all fields are inherited from AccountSummaryBase
    pass


__all__ = ("CalculatedAccountState",)
