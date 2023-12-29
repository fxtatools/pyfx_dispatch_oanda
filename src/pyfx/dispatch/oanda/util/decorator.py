"""Decorator model"""

from functools import partial
from itertools import chain
import warnings

from typing import Any, Callable, Generic, Optional, Union
from typing_extensions import (
    TYPE_CHECKING, ClassVar, Self, TypeAlias, TypeVar,
    get_args, get_origin, get_original_bases
)


T_decorated = TypeVar("T_decorated", bound=Union[Callable, type[type]])

T_self = TypeVar("T_self")

DecoratorCallback: TypeAlias = Callable[[T_decorated, Optional[tuple], Optional[dict[str, Any]]], T_self]


class Decorator(Generic[T_decorated]):
    """Generic base class for decorator classes
    """

    if TYPE_CHECKING:
        __decorating__: ClassVar[type]

    @classmethod
    def decorating(cls, obj) -> Optional[bool]:
        #
        # Try to determine the type of objects decorated with this Decorator
        # class, using generic type args for Decorator[T_decorated] within base
        # classes of the implementing class
        #
        # If the class variable __decorating__ is defined, return true if the
        # object is an instance of the type denoted in the __decorating__ attr
        #
        # Else:
        #
        # If the decorated type can be determined from generic type parameters,
        # then return a boolean value indicating whether the object matches the
        # first of the matching generic type args.
        #
        # If the decorated type cannot be determined from generic type args,
        # emit a warning and return None
        #
        # e.g for a class subclassing Decorator[<type>] then try to ensure
        # that  the  object - which may be an object to decorate - represents
        # a type object. This test may be fairly inexact, albeit, given the
        # nature of generic type parameters.
        #
        # for Decorator[Callable] the test may be more inexact, given the
        # generally Callable nature of a type name.
        #
        # An implementing Decorator class may provide a test for the type
        # of the first arg in __init__(decorated, ...)
        #
        if hasattr(cls, "__decorating__"):
            test = cls.__decorating__
        else:
            bounds = chain.from_iterable(get_args(b) for b in get_original_bases(cls) if isinstance(get_origin(b), type) and issubclass(get_origin(b), Decorator))
            test = next(bounds, None)

        if test:
            cls.__decorating__ = test
            try:
                # FIXME needs test for type-bounded Decorator classes
                # e.g class decorators, given a bound e.g 'type'
                if isinstance(test, type) and isinstance(obj, type):
                    return issubclass(obj, test)
                # FIXME needs test for func-bounded decorator classes
                # - toplevel funcs (decorator should be callable)
                # - class and instance method funcs (decorator should be callable)
                # - descriptor funcs, for some descriptor class
                #   using Decorator as a base class
                elif isinstance(obj, test):
                    return True
                else:
                    return False
            except TypeError:
                return False
        else:
            warnings.warn("No type bound for decorator test: %s" % (cls.__name__),
                          stacklevel=4)
            return None

    @classmethod
    def decorate(cls, *args, **kw) -> Union[Self, DecoratorCallback[T_decorated, Self]]:
        if not kw and len(args) == 1 and cls.decorating(args[0]):
            #
            # called as @decorator
            #
            # dispatch to decorate_new(decorated)
            #
            return cls.decorate_new(args[0])
        else:
            #
            # called as @decorator(...)
            #
            # return a function that will will decorate the object
            # that the args-based @decorator(...) expr is being
            # applied to, such that the function will dispatch
            # to decorate_new(decorated, ...)
            #
            return cls.decorate_args(args, kw)

    @classmethod
    def decorate_new(cls, decorated: T_decorated,
                     argdata: Optional[tuple[tuple, dict[str, Any]]] = None,
                     ) -> Self:
        if argdata is None:
            return cls(decorated)
        else:
            #
            # argdata: tuple of (positional_args, {kw: kwarg})
            # where positional_args would also be a tuple.
            #
            # either element may be empty
            #
            args = argdata[0]
            kw = argdata[1]
            return cls(decorated, *args, **kw)

    @classmethod
    def decorate_args(cls, *args: tuple[tuple, dict[str, Any]]) -> DecoratorCallback[T_decorated, Self]:

        def decorate_cb(cls, args, decorated) -> Self:
            return cls.decorate_new(decorated, argdata=args or None)

        return partial(decorate_cb, cls, args)


__all__ = ("Decorator",)
