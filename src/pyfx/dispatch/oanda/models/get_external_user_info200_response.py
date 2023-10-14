
"""model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from .user_info_external import UserInfoExternal

from ..transport import ApiObject, TransportField
from ..util import exporting


class GetExternalUserInfo200Response(ApiObject):
    """
    GetExternalUserInfo200Response
    """
    user_info: Annotated[Optional[UserInfoExternal], TransportField(None, alias="userInfo")]


__all__ = exporting(__name__, ...)
