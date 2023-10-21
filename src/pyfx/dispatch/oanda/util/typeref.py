"""support for type references"""

from .naming import exporting

from types import NoneType
from typing import Annotated, Literal, Union
from typing_extensions import ForwardRef, TypeAlias, TypeVar, get_args, get_origin


def get_literal_value(spec: TypeAlias):
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


def get_type_class(spec: Union[type, TypeAlias]) -> type:
    if isinstance(spec, type):
        return spec
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
            if args and len(args) is int(2) and args[-1] == NoneType:
                return get_type_class(args[0])
        elif isinstance(spec, TypeVar):
            bound = spec.__bound__
            if bound:
                if isinstance(bound, str):
                    bound = resolve_forward_reference(bound)
                return get_type_class(bound)
    raise ValueError("Unable to determine a concrete class for type", spec)


__all__ = tuple(exporting(__name__, ...))
