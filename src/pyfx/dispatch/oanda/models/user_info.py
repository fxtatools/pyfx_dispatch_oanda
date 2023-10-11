
"""model definition for OANDA v20 REST API (3.0.25)"""




from typing import Optional



from ..transport import ApiObject, TransportField
from ..util import exporting



class UserInfo(ApiObject):
    """
    A representation of user information, as provided to the user themself.
    """
    username: Optional[str] = TransportField(None)
    """
    The user-provided username.
    """
    user_id: Optional[int] = TransportField(None, alias="userID")
    """
    The user's OANDA-assigned user ID.
    """
    country: Optional[str] = TransportField(None)
    """
    The country that the user is based in.
    """
    email_address: Optional[str] = TransportField(None, alias="emailAddress")
    """
    The user's email address.
    """


__all__ = exporting(__name__, ...)

