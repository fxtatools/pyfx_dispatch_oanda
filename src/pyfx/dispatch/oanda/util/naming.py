## naming.py

from abc import abstractmethod
import enum
import sys
from types import ModuleType
from typing import (
    Any,
    Callable,
    Generator,
    Iterable,
    Iterator,
    Optional,
    Union,
)
from typing_extensions import Protocol, runtime_checkable, TypeAlias, TypeVar, get_type_hints
import typing

ModuleLike: TypeAlias = Union[str, ModuleType]
"""Generic type alias for a module identifier

Syntax: Module name, as a string, or a module object
"""


Tname = TypeVar("Tname", bound=str)


@runtime_checkable
class SupportsName(Protocol[Tname]):  # type: ignore
    @abstractmethod
    def __name__(self) -> Tname:
        raise NotImplementedError(self.__name__)


NameLike: TypeAlias = Union[str, SupportsName]


def is_type_var(value) -> bool:
    if hasattr(typing, "TypeVar"):
        tv_typing = getattr(typing, "TypeVar")
        if isinstance(value, tv_typing):
            return True
        else:
            return False
    elif isinstance(value, TypeVar):
        return isinstance(value, TypeVar)
    else:
        return False


def is_enum_member(value) -> bool:
    if isinstance(value, enum.Enum):
        ## generally this should also address the case of aenum.Enum
        return True
    return False


def names_iter(first: Union[NameLike, Iterable[NameLike]],
               *rest: Iterable[Union[NameLike, Iterable[NameLike]]],
               ) -> Iterator[str]:
    if isinstance(first, str):
        yield first
    ## checking for the generator type, before returning a generator's name
    elif isinstance(first, Generator):
        for name in first:
            yield from names_iter(name)
    elif hasattr(first, "__qualname__"):
        yield first.__qualname__
    ## StrEnum members will be presented by value, shortly
    elif isinstance(first, SupportsName):
        yield first.__name__  # type: ignore
    elif isinstance(first, Iterable):
        ## Python enums are iterable and classes,
        ## thus this is checked after
        ## the __qualname__/__name__ check
        for name in first:
            yield from names_iter(name)
    else:
        ## in effect, skipping any non-string object having no __name__ attr,
        ## in the object names iterator
        pass
    for name in rest:
        yield from names_iter(name)


def get_module(qual: ModuleLike) -> ModuleType:
    if isinstance(qual, ModuleType):
        return qual
    elif qual in sys.modules:
        return sys.modules[qual]
    else:
        raise ValueError("Unknown module", qual)


def module_defines(module: ModuleLike, *,
                   predicate: Optional[Callable[[Any], bool]] = None,
                   exclude: Optional[Union[Iterable[Any], Any]] = None,
                   exclude_types: Optional[Union[type, Iterable[type]]] = None,
                   annotations: Optional[bool] = True,
                   typevars=False, enum_members=False
                   ) -> Iterable[Any]:
    def check_val(val):
        if exclude and val in exclude:
            return False
        if predicate and not predicate(val):
            return False
        if not typevars and is_type_var(val):
            return False
        if not enum_members and is_enum_member(val):
            return False
        if exclude_types:
            cls = val.__class__
            for t in exclude_types:
                if issubclass(cls, t):
                    return False
        return True

    m = get_module(module)
    if exclude and not isinstance(exclude, Iterable) or isinstance(exclude, enum.Enum):
        exclude = (exclude,)
    if exclude_types and not isinstance(exclude_types, Iterable):
        exclude_types = {exclude_types}
    for val in m.__dict__.values():
        # fmt: off
        if hasattr(val, "__module__"):
            m_v = val.__module__
            if m_v in sys.modules and sys.modules[m_v].__name__ == m.__name__ and check_val(val):
                yield val
        # fmt: on
    if annotations:
        for name in get_type_hints(m).keys():
            try:
                v = getattr(m, name)
            except Exception:
                continue
            if check_val(v):
                ## Implementation Note:
                ## This will not return the annotation value itself,
                ## rather the annotation name
                yield name


def exporting(whence, first, *rest,
              predicate: Optional[Callable[[Any], bool]] = None,
              exclude: Optional[Union[Iterable[Any], Any]] = None,
              exclude_types: Optional[Union[type, Iterable[type]]] = None,
              annotations: bool = True, typevars: bool = False,
              enum_members: bool = False
              ) -> tuple[str]:
    m = get_module(whence)
    has_all = hasattr(m, "__all__")
    if first == ...:
        if has_all:
            iter_names = None
        else:
            iter_names = names_iter(
                module_defines(
                    m,
                    predicate=predicate,
                    exclude=exclude,
                    exclude_types=exclude_types,
                    annotations=annotations,
                    typevars=typevars,
                    enum_members=enum_members,
                ))
    else:
        iter_names = names_iter(rest)
    if has_all:
        if isinstance(m.__all__, list):
            to_exp = m.__all__.copy()
        else:
            to_exp = list(m.__all__)
    else:
        to_exp = []
    if first != ...:
        to_exp.extend(names_iter(first))
    if not has_all:
        to_exp.extend(iter_names)
    return tuple(set(to_exp))


__all__ = exporting(__name__, ...)
