"""FieldInfo generalization for applications"""

from pydantic.fields import FieldInfo
from typing import Callable
from typing_extensions import TypeVar


class ApplicationFieldInfo(FieldInfo):
    """Generalized FieldInfo base class"""
    __slots__ = tuple(frozenset(list(FieldInfo.__slots__) + [
        "defining_class", "name"
    ]))

    defining_class: type
    name: str

    def bind(self, field_name: str, cls: type):
        """Set the field name and defining class for this field info object"""
        self.name = field_name
        self.defining_class = cls


def ApplicationField(default, **kw):
    return ApplicationFieldInfo.from_field(default=default, **kw)


T_co = TypeVar("T_co", covariant=True)


def ApplicationFactoryField(default_factory: Callable[[], T_co], **kw):
    return ApplicationFieldInfo.from_field(default_factory=default_factory, **kw)


__all__ = "ApplicationFieldInfo", "ApplicationField", "ApplicationFactoryField"
