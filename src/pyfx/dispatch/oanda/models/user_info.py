"""UserInfo model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField


class UserInfo(ApiObject):
    """
    A representation of user information, as provided to the user themself.

    [**Deprecated**]

    This class was produced from definitions in the fxTrade v20 API 3.0.25.

    No known usage exists in the present edition of the v20 API
    """

    username: Annotated[Optional[str], TransportField(None)]
    """
    The user-provided username.
    """

    user_id: Annotated[Optional[int], TransportField(None, alias="userID")]
    """
    The user's OANDA-assigned user ID.
    """

    country: Annotated[Optional[str], TransportField(None)]
    """
    The country that the user is based in.
    """

    email_address: Annotated[Optional[str], TransportField(None, alias="emailAddress")]
    """
    The user's email address.
    """


__all__ = ("UserInfo",)
