"""Tag model definition"""

from typing import Annotated, Optional
from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField


class Tag(ApiObject):
    """A tag associated with an entity.

    supplemental to v20 3.5.0
    """
    
    type: Annotated[Optional[str], TransportField(None)]
    """"The type of the tag"""

    name: Annotated[Optional[str], TransportField(None)]
    """The name of the tag"""

__all__ = ("Tag",)
