
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Annotated, Optional


from .user_info import UserInfo

from ..transport import ApiObject, TransportField
from ..util import exporting


class GetUserInfo200Response(ApiObject):
    """
    GetUserInfo200Response
    """
    user_info: Annotated[Optional[UserInfo], TransportField(None, alias="userInfo")]


__all__ = exporting(__name__, ...)
