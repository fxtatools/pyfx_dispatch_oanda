
"""AccountProperties model definition for OANDA v20 REST API (3.0.25)"""

from typing import Optional

from ..transport import ApiObject, TransportField

class AccountProperties(ApiObject):
    """
    Properties related to an Account.
    """

    id: Optional[str] = TransportField(None)
    """The Account's identifier
    """
    mt4_account_id: Optional[int] = TransportField(None, alias="mt4AccountID")
    """The Account's associated MT4 Account ID. This field will not be present if the Account is not an MT4 account.
    """
    tags: Optional[list[str]] = TransportField(None)
    """The Account's tags
    """


__all__ = ("AccountProperties",)
