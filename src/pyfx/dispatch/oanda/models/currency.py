"""Currency defininition for applications"""

from aenum import Enum, extend_enum
from typing import Self
import isocodes

from ..transport.repository import ApiJsonEncoder

from ..transport import TransportEnumString, JsonTypesRepository


class Currency(Enum):
    """
    Currency identifier, ISO 4217 coding

    Values in the Currency enum class are derived from the `isocodes.currency` table.

    Implementation and Usage:

    Each Currency enum instance is indexed principally by its ISO 4217 three letter alphabetical code. This value may be accessed with the `name` or `alpha` property accessor on each enum instance.

    The corresponding ISO 4217 numerical code may be accessed with the `value` property on each instance, or indirectly via the `digits` property.

    A descriptive name for the representative Currency (EN) may be accessed via the `description` property on the Currency enum instance.

    Enum members can be located using a subscript accessor, provided the unique alphabetical code for the representative currency.

    ```python
    >>> Currency['CHF']
    <Currency.CHF: 756>
    ```

    A functional syntax is also available for accessing a Currency enum member, given the currency's unique alphabetical code or unique numerical code.

    ```python
    >>> Currency.from_alpha('CHF')
    <Currency.CHF: 756>

    >>> Currency.from_digits(756) is Currency.from_alpha('CHF')
    True
    ```

    For purpose of iteration, the `Currency._member_map_` table provides a mapping of each three letter alphabetical code to the corresponding Currency enum instance.

    The `Currency._value2member_map_` table provides a converse mapping from numerical codes to each Currency enum instances.

    Property accessors:
    - Currency.name -> str
    - Currency.alpha -> str
    - Currency.value -> int
    - Currency.numeric-> int
    - Currency.description -> str

    Class methods:
    - Currency.from_alpha(alpha: str) -> Currency
    - Currency.from_digits(digits: int) -> Currency

    Compatibility:

    The three digit ISO 4217 numerical code represents an unsigned integer with a maximum value of 999, compatible with `numpy.ushort`
    """

    def __str__(self) -> str:
        return self.name

    @property
    def alpha(self) -> str:
        """
        Return the ISO 4217 three letter alphabetical code for the representative currency.

        This value may be accessed directly via the `name` property on the enum instance.
        """
        return self.name

    @property
    def digits(self) -> int:
        """
        Return the ISO 4217 three digit numerical code for the representative currency.

        This value may be accessed directly via the `value` property on the enum instance.
        """
        return self.value

    @property
    def description(self) -> str:
        """
        Return a descriptive name (EN) for the representative currency.

        This property's value is cached dynamically from the `isocodes.currency` table, on first access for each enum member.
        """
        if hasattr(self, "_description"):
            return self._description
        else:
            desc = isocodes.currencies.by_alpha_3(self.name)['name']
            self._description = desc
            return desc

    def __index__(self) -> int:
        """Return the three digit numerical code for this Currency enumber member"""
        return self.value

    @classmethod
    def from_alpha(cls, name: str) -> Self:
        """Return the Currency member for a three letter alphabetical code"""
        return cls.__getitem__(name)

    @classmethod
    def from_digits(cls, digits: int) -> Self:
        """Return the Currency member for a three digit numerical code"""
        return cls._value2member_map_[digits]


class TransportCurrencyKind(TransportEnumString[Currency, str]):
    @classmethod
    def unparse(cls, venum: Currency, encoder: ApiJsonEncoder) -> str:
        return venum.alpha


JsonTypesRepository.bind(Currency, TransportCurrencyKind)


for dct in isocodes.currencies.items:
    name = dct["alpha_3"]
    digits = int(dct["numeric"])
    extend_enum(Currency, name, digits)

__all__ = ("Currency",)
