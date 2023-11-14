"""Supplemental transport type definitions"""

from .common_types import DoubleConstants
from ..transport.transport_base import TransportFloatStr, TransportFloatStrType


class TransportDecmialAll(TransportFloatStr, metaclass=TransportFloatStrType):
    """Transport type interface for values encoded with the symbolic
    alias`"ALL"` or as a decimal string.

    This transport type will interpret `"ALL"` as `numpy.inf`, and any
    other value as a decimal string. The string will be parsed as denoting
    a `numpy.double` value

    The parser interpretation is symmetrical onto `unparse_py()`

    Known Limitations
    - Not tested on 32 bit systems

    Applications
    - Generally applied for interpretation of unit values in  order
      close transactions

    See Also
    - TransportDecimalAllNone
    """

    @classmethod
    def parse(cls, value: str | float) -> float:
        if isinstance(value, float):
            return value
        elif value == "ALL":
            return DoubleConstants.INF.value  # type: ignore
        else:
            return super().parse(value)

    @classmethod
    def unparse_py(cls, value: float) -> str:
        if value == DoubleConstants.INF:
            return "ALL"
        else:
            return super().unparse_py(value)


class TransportDecimalAllNone(TransportFloatStr, metaclass=TransportFloatStrType):
    """Transport type ifor encoding symoblic value aliases
    and literal decimal values, given the possible aliases
    `"ALL"` and  `"NONE"`.

    This transport type will interpret the transport string `"ALL"`
    as `numpy.inf`, `"NONE"` as a common zero value of type
    `numpy.double`, and any other value as a string-encoded
    representation of a  decimal value. All values will be stored
    internally as of the type `numpy.double`

    In the interest of portability, the transport type is defined
    with a Python `float` interface. The values will be initialized
    as numpy floating point values, generally of the host's `numpy.double`
    type, compatible with Python `float`.

    Known Limitations
    - Not tested on 32 bit systems

    Applications
    -  ClosePositionRequest units

    See Also
    - TransportDecmialAll
    """
    @classmethod
    def parse(cls, value: str | float) -> float:
        if isinstance(value, float):
            return value
        elif value == "ALL":
            return DoubleConstants.INF.value  # type: ignore[attr-defined]
        elif value == "NONE":
            return DoubleConstants.ZERO.value  # type: ignore[attr-defined]
        else:
            return super().parse(value)

    @classmethod
    def unparse_py(cls, value: float) -> str:
        if value == DoubleConstants.ZERO:
            return "NONE"
        elif value == DoubleConstants.INF:
            return "ALL"
        else:
            return super().unparse_py(value)


__all__ = ("TransportDecmialAll", "TransportDecimalAllNone",)
