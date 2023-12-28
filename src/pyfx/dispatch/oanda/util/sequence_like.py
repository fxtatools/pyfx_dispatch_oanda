"""Sequence type utilities"""

from typing import Sequence
from typing_extensions import get_origin

def is_sequence_or_set_type(expr) -> bool:
    if isinstance(expr, type):
        # in Python releases previous to 3.11, the expression
        # `list[str]` is interpreted as a type. The get_origin()
        # call may serve to determine whether the type is a
        # type alias in this case.
        origin = get_origin(expr)
        if origin is None:
            return issubclass(expr, Sequence) or issubclass(expr, set)
        else:
            return is_sequence_or_set_type(origin)
    else:
        return False

__all__ = ("is_sequence_or_set_type",)
