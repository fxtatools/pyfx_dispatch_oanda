"""support for type references"""

from .naming import exporting

from abc import ABC, ABCMeta
from typing import Annotated, Any, Literal, Union, _SpecialForm
from typing_extensions import ForwardRef, TypeVar, get_args, get_origin


class TypeRefType(ABCMeta):
    """Abstract TypeRef metaclass"""
    def __instancecheck__(cls, obj: Any) -> bool:
        """Instance check for TypeRef

        Return true if the object is a type or a TypeAlias object

        Known limitations:

        - The type implementation of aliases in Python 3.11 differs
          substantially to how type aliases are implemented in earlier
          Python releases.

          For example:

          - In Python 3.10, the expression `list[int]`  will be parsed as
            a type reference, e.g `(list[int]).__class__ =>  <class 'type'>`

          - In Python 3.11: `(list[int]).__class__ => types.GenericAlias`

          In the Python 3.10 case, the object parsed from the `list[int]`
          expression may be handled as a type under `isinstance()`. However,
          it may sometimes result in error if the object is used as the first
          arg for `issubclass()`. This may be generally the case when the
          second arg to this `issubclass()` class would represent a user-
          defined class.

          In Python releases previous to 3.11 this method will not be able
          detect the exact distinction of whether an object represents a
          type or a type alias. This difference in implementation should
          not result in different  behaviors for the instance check
          described here.

        - If applied for example in parsing a type alias arg,  this function will
          not dereference any forward reference string denoting a type

        See also: `resolve_forward_reference()`
        """
        return isinstance(obj, type) or (isinstance(obj, _SpecialForm) and obj.__name__ == "TypeAlias")


class TypeRef(ABC, metaclass=TypeRefType):
    """Abstract representation of types and type alias objects
    """

def get_literal_value(spec: TypeRef):
    if get_origin(spec) == Annotated:
        return get_literal_value(get_args(spec)[0])
    elif get_origin(spec) == Literal:
        return get_args(spec)[0]
    else:
        raise ValueError("Not a literal type reference", spec)


def resolve_forward_reference(ref: str, **localvars):
    fwd = ForwardRef(ref)
    use_locals = locals().copy()
    use_locals.update(localvars)
    try:
        return fwd._evaluate(globals(), use_locals, frozenset())
    except Exception as exc:
        raise ValueError("Unable to resolve forward reference", ref) from exc


def get_type_class(spec: Union[type, TypeRef]) -> type:
    if isinstance(spec, type):
        # portability for Python 3.10 and earlier releases
        # where the expression `list[int]`` is interpreted
        # as an incomplete type
        origin = get_origin(spec)
        if origin is None:
            return spec
        else:
            return get_type_class(origin)
    elif isinstance(spec, str):
        return get_type_class(resolve_forward_reference(spec))
    ## FIXME if it's a 'literal' type, return the type of the value
    else:
        origin = get_origin(spec)
        if origin and isinstance(origin, type):
            ## Known limitation: This will collapse information
            ## from any generic Sequence type alias
            return origin
        elif origin == Literal:
            return get_literal_value(spec).__class__
        elif origin == Union:
            args = get_args(spec)
            ## parse a stored type alias from an Optional[typedecl] declaration
            if args and len(args) is int(2) and args[-1] == None.__class__:
                return get_type_class(args[0])
        elif isinstance(spec, TypeVar):
            bound = spec.__bound__
            if bound:
                if isinstance(bound, str):
                    bound = resolve_forward_reference(bound)
                return get_type_class(bound)
    raise ValueError("Unable to determine a concrete class for type", spec)


__all__ = "TypeRef", "get_literal_value", "resolve_forward_reference", "get_type_class"
