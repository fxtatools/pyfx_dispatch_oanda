"""Price components for instrument candlestick requests"""

from typing import Union
from ..util.sequence_like import SequenceLike

from ..mapped_enum import MappedEnum, MappedEnumType


class PriceComponentType(MappedEnumType):
    def __getitem__(cls, key: Union[str, SequenceLike[str]]) -> str:
        return cls.get(key)


class PriceComponent(str, MappedEnum, metaclass=PriceComponentType):
    """Enum for instrument candlestick requests"""

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
    def get(cls, ident: Union[str, SequenceLike[str]]) -> "PriceComponent":
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

    def __or__(self, value: Union[str, "PriceComponent"]) -> str:
        lhval = self.value
        rhval = self.__class__.get(value) if isinstance(value, str) else value.name  # type: ignore
        args = "".join(set(lhval + rhval))
        return self.__class__.get(args)


__all__ = "PriceComponent", "PriceComponentType"
