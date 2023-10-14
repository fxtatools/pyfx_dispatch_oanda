
"""model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional


from .account_properties import AccountProperties
from typing import Annotated, Optional


from ..transport import ApiObject, TransportField
from ..util import exporting


class ListAccounts200Response(ApiObject):
    """
    listAccounts200Response
    """
    accounts: Annotated[Optional[list[AccountProperties]], TransportField(None)]
    """
    The list of Accounts the client is authorized to access and their associated properties.
    """


__all__ = exporting(__name__, ...)
