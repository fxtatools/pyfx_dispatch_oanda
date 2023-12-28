"""Abstract Finalizable classes"""

from abc import ABC, ABCMeta
from contextlib import contextmanager
from enum import Enum
from typing import Any
from typing_extensions import Self

class FinalizationState(Enum):
    NONE = "NONE"
    FINALIZED = "FINALIZED"
    DEFERRED = "DEFERRED"
    NEVER = "NEVER"


class Finalizable(ABC):
    __finalize__: bool = False
    """If true, finalize this object during initialization"""

    __finalization_state__: FinalizationState = FinalizationState.NONE
    """Finalization state"""

    @property
    def __finalized__(self) -> bool:
        """Return True if `self` is in a finalized state"""
        return self.__finalization_state__ == FinalizationState.FINALIZED

    @property
    def __finalizing__(self) -> bool:
        """Return True if the object is in an intermediate finalization state.

        This property's value will be True generally when the `__finalization_state__`
        for the object is `FinalizationState.DEFERRED` or when the object has a _truthy_
        value for `self.__finalize__` and the object is not yet finalized"""
        if self.__finalization_state__ == FinalizationState.NEVER:
            return False
        elif self.__finalization_state__ == FinalizationState.DEFERRED or (
            self.__finalize__ and not self.__finalized__
        ):
            return True
        else:
            return False

    @contextmanager
    def __finalization__(self):
        """Yield the object, then finalize if appliacble.

        If the `__finalizing__` property for the object is true, then the
        `__finalization_state__` for the object will be set to
        `FinalizationState.FINALIZED`, after the object is yielded by the
        context manager.

        Subclasses may extend this method, implementing any custom finalization
        logic before yield and/or before return from the context manager, mainly
        when `self.__finalizing__` is true. If `self.__finalizing__` is not true,
        the implementing context manager should yield the object without further
        finalization.

        This context manager is used in the implementation for
        `__finalize_instance__()`
        """
        yield self
        if self.__finalizing__:
            self.__finalization_state__ = FinalizationState.FINALIZED

    def __finalize_instance__(self):
        """Finalize the object.

        If the object is not yet finalized, the `__finalization_state__` for the
        object will be set to `FinalizationState.DEFERRED` then the object will be
        processed with the `__finalization__` context manager and returned.
        Otherwise, the  object will be returned without further processing for
        finalization

        Subclasses may extend this method.

        Generally, the subclass should extend at most one one of the
        `__finalization__()`  context manager  or `__finalize_instance__()`
        """
        if self.__finalized__ or self.__finalization_state__ == FinalizationState.NEVER:
            return
        self.__finalization_state__ = FinalizationState.DEFERRED
        with self.__finalization__():
            return self


class FinalizableClass(Finalizable, ABCMeta):

    def __new__(mcls: type[Self], name: str, bases: tuple[type, ...], attrs: dict[str, Any], **kw) -> Self:
        new_cls = super().__new__(mcls, name, bases, attrs, **kw)
        if new_cls.__finalize__:
            new_cls.__finalize_instance__()
        return new_cls


__all__ = "FinalizationState", "Finalizable", "FinalizableClass"
