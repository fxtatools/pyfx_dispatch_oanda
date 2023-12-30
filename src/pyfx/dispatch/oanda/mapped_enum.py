"""Enum classes extending aenum in application of immutables.Map"""

from contextlib import contextmanager
from typing import TYPE_CHECKING, Iterator
from typing_extensions import ClassVar
from aenum import Enum, EnumType, extend_enum   # type: ignore[import-untyped]
from immutables import Map
from .finalizable import FinalizationState, Finalizable

from typing import Any, Callable, Iterable, Union
from typing_extensions import Self


class MappedEnumType(Finalizable, EnumType):

    if TYPE_CHECKING:
        _member_map_: Union[dict[str, Any], Map[str, Any]]
        """See also: MappedEnum. _member_map_"""

        _value2member_map_: Union[dict[str, Any], Map[str, Any]]
        """See also: MappedEnum._value2member_map_"""

        _member_names_: Union[list[str], tuple[str, ...]]
        """See also: MappedEnum._member_names_"""

        _missing_value_: Callable[[Any], "MappedEnum"]
        """See also: MappedEnum._missing_value_"""

    @property
    def __members__(cls) -> Union[dict, Map]:
        """Iterable mapping of enum member names to enum objects

        In extension to `aenum.Enum._`__members__`: After the MappedEnum
        is finalized, the return value will represent the Enum's immutable
        `_member_map_` object itself, rather than a copy of the `_member_map_`.

        When not finalized, this method will retain the behavior defined in
        `aenum.Enum`, in which the return value will comprise a copy of the
        `_member_map_` for the defininig Enum.
        """
        if cls.__finalized__:
            return cls._member_map_
        else:
            return cls._member_map_.copy()  # type: ignore

    @contextmanager
    def __finalization__(cls):
        """Finalize the enum class, if not already finalized.

        This method is called generally at the enum type scope, after applying
        any `__gen__` generator,  for MappedEnum classes defined with
        `__finalize__:  ClassVar[bool] == True`

        When finalizing the enum class `cls`, this method will replace a
        small number of mutable `aenum.Eeum` properties with mutable
        properties. Mainly, the following:

        - Each of the `_member_map_`  and `_value2member_map_` mappings will
          be replaced with an `immutables.Map`

        - The `_member_names_` sequence will be replaced with a tuple

        Subsequent of finalization, the enum class cannot be further
        extended as with `aenum.extend_enum()`
        """
        # if not cls.__finalized__:
        with super().__finalization__():
            cls._member_map_ = Map(cls._member_map_)  # type: ignore[misc]
            cls._value2member_map_ = Map(cls._value2member_map_)
            cls._member_names_ = tuple(cls._member_names_)
            cls.__finalization_state__ = FinalizationState.DEFERRED
            yield cls

    def __new__(mcls, name, *args, **kw):
        """Define a new MappedEnumType, or dereference the value of an existing
        mapped enum

        ### Constructor as Dereference Call

        As a convention, `args` and `kw` may be empty in a call to the enum `__new__`
        method, such as in a call form for dereferencing a value of an existing enum
        class. When `__new__` would be called within such a call form, 'metacls' would
        denote the enum  class and the enum value would be provided as `name`

        ### Value Generation

        A `__gen__` argument may be provided when a new MappedEnum class is defined.

        If provided as a callable value, the `_gen__` value will be applied in the
        form of a class method. The function should produce an iterator for producing
        member values in the new class.

        If not provided as a callable value, the `__gen__` value should represent
        a generator object.

        Whether implemented with a function or provided as a generator object, the
        `__gen__` generator should produce a series of individual sequence values,
        suitable as member args in a call to `extend_enum()` provided after the new
        enum class.

        The `__gen__` value will be applied only during class initialization. The
        value will be removed from the `__dict__` for the defining MappedEnum
        class.

        ## Finalization

        If a `__finialized__` parameter is provided with a true value when the
        MappedEnum class is defined, the class' `finalize()` method will be called
        before the new class is returned from this method.

        if a `__gen__` iterator has been provided, `finalize()` will be called
        not until after the iterator has been applied.
        """
        zero = int(0)
        if len(args) is zero and len(kw) is zero:
            return mcls[name]  # type: ignore
        else:
            attrs = args[1]
            # note also: _missing_value_ handling under aenum
            gen = attrs.get("__gen__", False)
            if gen:
                if __debug__:
                    if not isinstance(gen, (Callable, Iterable,)):  # type: ignore[arg-type]
                        raise AssertionError("__gen__ value is neither callable nor iterable", gen)
                del attrs["__gen__"]
            to_finalize = attrs.get("__finalize__", False)
            if to_finalize:
                del attrs["__finalize__"]

            new_cls: Self = super().__new__(mcls, name, *args)

            if gen:
                for args in (gen(new_cls) if callable(gen) else gen):
                    extend_enum(new_cls, *args)

            if to_finalize:
                new_cls.__finalize_instance__()

            return new_cls

    def __getitem__(cls, name):
        if name in cls._member_names_:
            return cls._member_map_[name]
        raise KeyError("Enum member not found", name)

    def __getattr__(cls, name):
        if name in cls._member_names_:
            return cls._member_map_[name]
        elif name == "__members__" and "__members__" not in cls.__dict__:
            # weird hack for enum class __members__ access for Pydantic,
            # after the __members__ property has appeared to be nonexistent
            # for some enum types defined with this class
            return cls._member_map_
        else:
            return super().__getattr__(name)

    def __iter__(self) -> Iterator[Self]:
        # the _member_names_ attr provides an index of member
        # names in order of definition. The _member_map_ attr
        # may represent an immutables.Map, such that may not
        # be similarly ordered.
        #
        # Separately, the iterator here is not reentrant
        members = self._member_map_
        return (members[name] for name in self._member_names_)


class MappedEnum(Enum, metaclass=MappedEnumType):


    if TYPE_CHECKING:

        _member_map_: ClassVar[Union[dict[str, Self], Map[str, Self]]]
        """Iterable mapping of enum member names to enum objects

        This value should generally not be modified external to
        the enum class definition.

        See also:
        - `MappedEnumType.__members__`, as in effect a property
            at the class scope, for MappedEnum definitions
        - `aenum.extend_enum()` for applications in runtime
            definition of an enum member
        """

        __members__: ClassVar[Union[dict[str, Self], Map[str, Self]]]
        """Iterable mapping of enum member names to enum objects

        See also: `_member_map_`
        """

        _value2member_map_: ClassVar[Union[dict[Any, Self], Map[Any, Self]]]
        """Iterable mapping of enum member values to enum objects

        In extension to `aenum.Enum._value2member_map_`: When the MappedEnum
        is finalized, this mapping will be defined  as an `immutables.Map`
        """

        _member_names_: ClassVar[Union[list[Any], tuple[Any, ...]]]
        """Sequence of enum member names

        In extension to `aenum.Enum._member_names_`: When the MappedEnum is
        finalized, this sequence will be defined as a tuple
        """

        _missing_value_: ClassVar[Callable[[Any], Self]]
        """Callable in the form of a static method, applied for enum value reference

        The `_missing_value_` function is introduced in aenum, such as for
        application when dereferncing an enum value via the constructor for
        the defining enum class. The function will be called in the form of
        a static method, with the provided enum value as its only arg, when
        the provided arg was not located in the set of existing enum member
        name..

        Within MappedEnum definitions, if a `_missing_value_` function is not
        provided in the class' definition, a `_missing_vlaue_` function will
        be defined  to dispatch to the class method `get()` for the defining
        enum class.
        """

    @classmethod
    def get(cls, arg):
        """Return any enum member, or raise ValueError

        If `arg` denotes a key in `cls._member_map_`, returns the value for that key,
        else raises `ValueError`
        """
        try:
            return cls._member_map_[arg]
        except KeyError as exc:
            raise ValueError("No enum member found for name", arg) from exc


__all__ = "MappedEnumType", "MappedEnum"
