"""CreateTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal, Optional

from ..transport import TransportField

from .transaction import Transaction
from .transaction_type import TransactionType
from .currency import Currency


class CreateTransaction(Transaction):
    """
    A CreateTransaction represents the creation of an Account.
    """

    type: Literal[TransactionType.CREATE] = TransportField(TransactionType.CREATE)
    """
    The Type of the Transaction. Always set to \"CREATE\" in a CreateTransaction.
    """

    division_id: Optional[int] = TransportField(None, alias="divisionID")
    """
    The ID of the Division that the Account is in
    """

    site_id: Optional[int] = TransportField(None, alias="siteID")
    """
    The ID of the Site that the Account was created at
    """

    account_user_id: Optional[int] = TransportField(None, alias="accountUserID")
    """
    The ID of the user that the Account was created for
    """

    account_number: Optional[int] = TransportField(None, alias="accountNumber")
    """
    The number of the Account within the site/division/user
    """

    home_currency: Optional[Currency] = TransportField(None, alias="homeCurrency")
    """
    The home currency of the Account
    """


__all__ = ("CreateTransaction",)
