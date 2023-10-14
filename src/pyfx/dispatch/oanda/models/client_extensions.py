
"""model definition for OANDA v20 REST API (3.0.25)"""




from typing import Annotated, Optional



from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting



class ClientExtensions(ApiObject):
    """
    A ClientExtensions object allows a client to attach a clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if your account is associated with MT4.
    """
    id: Annotated[Optional[str], TransportField(None)]
    """The Client ID of the Order/Trade
    """
    tag: Annotated[Optional[str], TransportField(None)]
    """A tag associated with the Order/Trade
    """
    comment: Annotated[Optional[str], TransportField(None)]
    """A comment associated with the Order/Trade
    """


__all__ = exporting(__name__, ...)

