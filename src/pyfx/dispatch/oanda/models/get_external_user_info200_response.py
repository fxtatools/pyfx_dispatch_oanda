"""[Deprecated] GetExternalUserInfo200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from .user_info_external import UserInfoExternal

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField


class GetExternalUserInfo200Response(ApiObject):
    """
    GetExternalUserInfo200Response

    [**Deprecated**]

    This class was produced from definitions in the fxTrade v20 API 3.0.25, with reference
    to a `users` endpoint. This endpoint is no longer available with fxTrade v20
    """
    user_info: Annotated[Optional[UserInfoExternal], TransportField(None, alias="userInfo")]


__all__ = ("GetExternalUserInfo200Response",)
