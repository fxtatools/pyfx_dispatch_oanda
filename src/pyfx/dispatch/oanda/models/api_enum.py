"""ApiEnum definition"""

from ..mapped_enum import MappedEnum, MappedEnumType


class ApiEnumType(MappedEnumType):
    def __finalize_instance__(cls):
        if not cls.__finalized__:
            for member in cls._member_map_.values():
                if not hasattr(member, "_bytes"):
                    member._bytes = member.value.encode()
            return super().__finalize_instance__()


class ApiEnum(str, MappedEnum, metaclass=ApiEnumType):
    """MappedEnum class for API string constants"""

    # __finalize__: ClassVar[Literal[True]] = True

    def __bytes__(self) -> bytes:
        return self._bytes

    def __str__(self) -> str:
        return self.name


__all__ = ("ApiEnumType", "ApiEnum",)
