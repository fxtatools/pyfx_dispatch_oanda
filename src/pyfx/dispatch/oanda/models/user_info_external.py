"""UserInfoExternal model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField

class UserInfoExternal(ApiObject):
    """
    A representation of user information, as available to external (3rd party) clients.

    [**Deprecated**]

    This class was produced from definitions in the fxTrade v20 API 3.0.25.

    No known usage exists in the present edition of the v20 API
    """

    user_id: Annotated[Optional[int], TransportField(None, alias="userID")]
    """
    The user's OANDA-assigned user ID.
    """

    country: Annotated[Optional[str], TransportField(None)]
    """
    The country that the user is based in.
    """

    fifo: Annotated[Optional[bool], TransportField(None, alias="FIFO")]
    """
    Flag indicating if the the user's Accounts adhere to FIFO execution rules.
    """

__all__ = ("UserInfoExternal",)
