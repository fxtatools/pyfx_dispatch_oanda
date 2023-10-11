
"""model definition for OANDA v20 REST API (3.0.25)"""




from typing import Optional


from .client_configure_transaction import ClientConfigureTransaction

from ..transport import ApiObject, TransportField
from ..util import exporting



class ConfigureAccount200Response(ApiObject):
    """
    ConfigureAccount200Response
    """
    client_configure_transaction: Optional[ClientConfigureTransaction] = TransportField(None, alias="clientConfigureTransaction")
    last_transaction_id: Optional[str] = TransportField(None, alias="lastTransactionID")
    """The ID of the last Transaction created for the Account.
    """


__all__ = exporting(__name__, ...)

