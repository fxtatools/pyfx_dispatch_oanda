"""ListAccounts200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from .account_properties import AccountProperties


class ListAccounts200Response(ApiObject):
    """
    listAccounts200Response
    """

    accounts: Annotated[list[AccountProperties], TransportField(...)]
    """
    The list of Accounts the client is authorized to access and their associated properties.
    """


__all__ = ("ListAccounts200Response",)
