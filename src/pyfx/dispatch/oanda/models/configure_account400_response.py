
"""model definition for OANDA v20 REST API (3.0.25)"""




from typing import Optional


from .client_configure_reject_transaction import ClientConfigureRejectTransaction

from ..transport import ApiObject, TransportField
from ..util import exporting



class ConfigureAccount400Response(ApiObject):
    """
    ConfigureAccount400Response
    """
    client_configure_reject_transaction: Optional[ClientConfigureRejectTransaction] = TransportField(None, alias="clientConfigureRejectTransaction")
    last_transaction_id: Optional[str] = TransportField(None, alias="lastTransactionID")
    """The ID of the last Transaction created for the Account.
    """
    error_code: Optional[str] = TransportField(None, alias="errorCode")
    """The code of the error that has occurred. This field may not be returned for some errors.
    """
    error_message: Optional[str] = TransportField(None, alias="errorMessage")
    """The human-readable description of the error that has occurred.
    """


__all__ = exporting(__name__, ...)

