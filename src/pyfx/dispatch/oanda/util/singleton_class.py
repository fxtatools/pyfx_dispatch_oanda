## SingletonClass definition

from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Generic
from typing_extensions import ClassVar, Self, TypeVar

T_co = TypeVar("T_co", covariant=True)

class SingletonClass(Generic[T_co], ABCMeta):

    @property
    def __singleton__(cls) -> Self:
        """Return the singleton instance for this class

        This property represents a deferred attribute accessor onto the
        base property, `__singleton_instance__`. If the base property has
        been initialized when this property descriptor is called, then the
        value of the base  property will be returned. Else, the base property
        will be initialized with the return value from the base property
        initializer,  `cls.initialize_singleton()` and that value returned.
        """
        if hasattr(cls, "__singleton_instance__"):
            return cls.__singleton_instance__
        else:
            singleton = cls.initialize_singleton()
            cls.__singleton_instance__ = singleton
            return singleton

    @abstractmethod
    def initialize_singleton(cls):
        """Return a value for access under the __singleton__ property of the class"""
        raise NotImplementedError(cls.initialize_singleton)

    def __new__(mcls: type[Self], name: str, bases: tuple[type, ...], attrs: dict[str, Any]) -> Self:
        """Ensure annotations for singleton class variables in the new SingletonClass

        For each of the attribute names `__singleton__`  and `__singleton_instance__`, when an
        annotation was not defined for that attribute name -- such as via the `attrs` namespace,
        or otherwise within the superclass'  `__new__` method -- then this method will define an
        annotation onto that attribute, as the attribute denoting a class variable of a type equal
        to the new class.
        """
        new_cls = super().__new__(mcls, name, bases, attrs)

        annot = new_cls.__annotations__
        if "__singleton__" not in annot:
            annot["__singleton__"] = ClassVar[new_cls]
        if "__singleton_instance__" not in annot:
            annot["__singleton_instance__"] = annot["__singleton__"]
        return new_cls

__all__ = ("SingletonClass",)
