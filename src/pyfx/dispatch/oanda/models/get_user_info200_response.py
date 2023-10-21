"""[Deprecated] GetUserInfo200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from .user_info import UserInfo

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField


class GetUserInfo200Response(ApiObject):
    """
    GetUserInfo200Response

    [**Deprecated**]

    This class was produced from definitions published in the fxTrade v20 API 3.0.25, with
    reference to a `users` endpoint. This endpoint is not available with the public interface
    for the fxTrade v20 API
    """

    user_info: Annotated[Optional[UserInfo], TransportField(None, alias="userInfo")]


__all__ = ("GetUserInfo200Response",)
