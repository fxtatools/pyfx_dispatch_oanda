"""Price components for instrument candlestick requests"""

from typing import Union, Iterable, TYPE_CHECKING
from typing_extensions import Self

from .api_enum import ApiEnum, ApiEnumType

class PriceComponentType(ApiEnumType):
    def __getitem__(cls, key: Union[str, Iterable[str]]) -> str:
        return cls.get(key)

class PriceComponent(ApiEnum, metaclass=PriceComponentType):
    """Enum for instrument candlestick requests"""

    if TYPE_CHECKING:
        value: str
        # url_string will be bound during component unparse, below
        url_string: str

    ASK = "A"
    """Candlestick summarization of Ask price"""

    BID = "B"
    """Candlestick summarization of Bid price"""

    MID = "M"
    """Candlestick summarization for median of Ask and Bid prices"""

    ASK_BID = "AB"
    """Candlestick summarizations of Ask and Bid prices"""

    ASK_MID = "AM"
    """Candlestick summarizations Ask and Median prices"""

    BID_MID = "BM"
    """Candlestick summarizations Bid and Median prices"""

    ALL = "ABM"
    """All Candlestick summarization prices"""

    @classmethod
    def get(cls, ident: Union[str, Iterable[str]]) -> "PriceComponent":
        """Return a the PriceComponent for  a string `ident`

        `ident` may represnt a name, value, or repeating string of values
        for a price component, in any combination of upper or lower case
        string encoding.

        raises KeyError if a value in `ident` cannot be interpreted as
        a PriceComponent

        ```python
        >>> PriceComponent.get("A")
         <PriceComponent.ASK: 'A'>

        >>> PriceComponent.get("bid")
        <PriceComponent.BID: 'B'>

        >>> PriceComponent.get("amabm")
        <PriceComponent.ALL: 'ABM'>
        ```
        """
        if not isinstance(ident, str):
            if __debug__:
                if not isinstance(ident, Iterable):
                    raise AssertionError("Not iterable", ident)
            ident = "".join(ident)
        ident_uc = ident.upper()
        members = cls._member_map_
        if ident_uc in members:
            return members[ident_uc]
        else:
            values = cls._value2member_map_
            if ident_uc in values:
                return values[ident_uc]
            elif isinstance(ident, str) and len(ident) > 1:
                ident_set = {c.upper() for c in ident}
                members = {cls.get(c) for c in ident_set}
                return cls.get("".join(sorted(member.value for member in members)))
            else:
                raise KeyError("PriceComponent not found", ident)

    @classmethod
    def unparse(cls, value: Union[str, Self]) -> str:
        if isinstance(value, cls):
            name = value.value


    def __or__(self, value: Union[str, "PriceComponent"]) -> str:
        lhval = self.value
        rhval = self.__class__.get(value) if isinstance(value, str) else value.name  # type: ignore
        args = "".join(set(lhval + rhval))
        return self.__class__.get(args)



__all__ = "PriceComponent", "PriceComponentType"
