"""TransportField definition"""

from .transport_base import TransportFieldInfo, TransportTypeInfer, TransportType, Ti, To

from typing import Optional

def TransportField(default, *,
                   transport_type: TransportType[Ti, To] = TransportTypeInfer,
                   alias: Optional[str] = None,
                   description: Optional[str] = None,
                   deprecated: bool = False,
                   **kw) -> TransportFieldInfo[Ti, To]:
    """Initialize and return a TransportFieldInfo for literal-typed JSON transport encoding"""
    return TransportFieldInfo.from_field(
        default,
        transport_type=transport_type,
        alias=alias,
        description=description,
        deprecated=deprecated,
        **kw)


__all__ = ("TransportField",)
