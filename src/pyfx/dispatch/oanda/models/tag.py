"""Tag model definition"""

from typing import Optional
from ..transport import ApiObject, TransportField


class Tag(ApiObject):
    """A tag associated with an entity.

    supplemental to v20 3.5.0
    """
    
    type: Optional[str] = TransportField(None)
    """"The type of the tag"""

    name: Optional[str] = TransportField(None)
    """The name of the tag"""

__all__ = ("Tag",)
