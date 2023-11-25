"""Currency Pair encoding for applications"""

from aenum import extend_enum  # type: ignore[import-untyped]
from ..finalizable import FinalizationState
from ..mapped_enum import MappedEnum


from types import NotImplementedType
from typing import Callable, Self, Union, TYPE_CHECKING
from typing_extensions import ClassVar

from .currency import Currency

CURRENCY_PAIR_BASE_SHIFT: int = 16
CURRENCY_PAIR_QUOTE_MASK: int = 0xffff


class CurrencyPair(MappedEnum):
    """
    Enum Representation of a Currency pair

    enum member name: a string representation of the currency
    pair, in a syntax BBBQQQ, such that BBB represents the
    base currency and QQQ represents the quote currency.

    enum member value: an integer representing the bitwse `or`
    of the base currency's three-digit numerical code shifted
    leftwards 16 bits and the quote currency's three-digit
    numerical code.

    The respective currency code values may be accessed with
    the property accessors `CurrencyPair.base_digits` and
    `CurrencyPair.quote_digits`

    Property accessors:
    - `CurrencyPair.name` -> the conctatenated name of the currency pair
    - `CurrencyPair.value` -> the integer code for the currency pair
    - `CurrencyPair.base_digits` -> digit code for the base currency
    - `CurrencyPair.quote_digits` -> digit code for the quote currency
    - `CurrencyPair.base_currency` -> Currency enum member representing the base currency
    - `CurrencyPair.quote_currency` -> Currency enum member representing the quote currency

    Class methods:

    - `CurrencyPair.from_str_pair(str, str)` : Retrieve a CurrencyPair from `base` and `quote` currency names

    - CurrencyPair.from_str(str) :  Retrieve a CurrencyPair for a concatenated currency pair name, e.g `AUDCHF`

    - CurrencyPair.from_delimited_str(str) :  Retrieve a CurrencyPair for a delimited currency pair name, e.g `AUD_CHF` or `AUD/CHF`
    """

    __finalization_state__: ClassVar[FinalizationState] = FinalizationState.NEVER

    if TYPE_CHECKING:
        name: str
        value: int

    @property
    def base_digits(self) -> int:
        """ISO 4217 numerical code representing the base currency"""
        if hasattr(self, "_base_currency"):
            return self._base_currency.digits  # type: ignore[has-type]
        else:
            return self.value >> CURRENCY_PAIR_BASE_SHIFT

    @property
    def quote_digits(self) -> int:
        """ISO 4217 numerical code representing the quote currency"""
        if hasattr(self, "_quote_currency"):
            return self._quote_currency.digits  # type: ignore[has-type]
        else:
            return self.value & CURRENCY_PAIR_QUOTE_MASK

    @property
    def base_currency(self) -> Currency:
        """The Currency object representing the base currency"""
        if hasattr(self, "_base_currency"):
            return self._base_currency  # type: ignore[has-type]
        else:
            base_digits = self.base_digits
            base = Currency.get(base_digits)
            self._base_currency = base
            return base

    @property
    def quote_currency(self) -> Currency:
        """The Currency object representing the quote currency"""
        if hasattr(self, "_quote_currency"):
            return self._quote_currency  # type: ignore[has-type]
        else:
            quote_digits = self.quote_digits
            quote = Currency.get(quote_digits)
            self._quote_currency = quote
            return quote

    @property
    def api_name(self) -> str:
        """Sstring representation of the currency pair for the v20 API"""
        if hasattr(self, "_api_name"):
            return self._api_name  # type: ignore[has-type]
        else:
            name = self.base_currency.name + "_" + self.quote_currency.name
            self._api_name = name
            return name

    @property
    def api_bytes(self) -> bytes:
        """Bytes representation of the currency pair for the v20 API"""
        if hasattr(self, "_api_bytes"):
            return self._api_bytes  # type: ignore[has-type]
        else:
            bstr = self.base_currency.name.encode() + b"_" + self.quote_currency.name.encode()
            self._api_bytes = bstr
            return bstr

    @classmethod
    def from_str_pair(cls, base: str, quote: str) -> Self:
        """Return the CurrencyPair for a set of base and quote currency symbols

        base: three-digit alphabetical code for the base currency, generally per ISO 4217
        quote: three-digit alphabetical code for the quote currency, generally per ISO 4217

        returns a CurrencyPair enum object representing currency pair
        """
        base_cur = Currency.get(base)
        quote_cur = Currency.get(quote)
        assert base_cur is not quote_cur, "base currency and quote currency are equivalent"
        code = (base_cur.digits << CURRENCY_PAIR_BASE_SHIFT) | quote_cur.digits
        codes_map = cls._value2member_map_
        if code in codes_map:
            return codes_map[code]
        else:
            name = base + quote
            inst = extend_enum(cls, name, code)
            inst._base_currency = base_cur
            inst._quote_currency = quote_cur
            inst._api_name = str(base_cur) + "_" + str(quote_cur)
            inst._api_bytes = bytes(base_cur) + b"_" + bytes(quote_cur)
            inst._hash_code = hash(code)
            return inst

    @classmethod
    def from_int(cls, code: int) -> Self:
        """
        Return the CurrencyPair for a CurrencyPair integer code

        code: a CurrencyPair integer code, as the bitwise union
        of integer codes for the base and quote currencies.

        To produce a currency pair integer code, the integer
        code for the base currency - generally per ISO 4217 -
        should be shifted leftwards 16 bits, then combined
        in a logical `or` with the bitwise representation
        of the integer code for the quote currency.

        returns the corresponding CurrencyPair
        """
        codes_map = cls._value2member_map_
        if code in codes_map:
            return codes_map[code]
        else:
            base_cur = Currency.get(code >> CURRENCY_PAIR_BASE_SHIFT)
            quote_cur = Currency.get(code & CURRENCY_PAIR_QUOTE_MASK)
            assert base_cur is not quote_cur, "base currency and quote currency are equivalent"
            name = base_cur.name + quote_cur.name
            inst = extend_enum(cls, name, code)
            inst._base_currency = base_cur
            inst._quote_currency = quote_cur
            return inst

    @classmethod
    def from_str(cls, name: str) -> Self:
        """
        Return the CurrencyPair for a concatenated name

        name: a concatenated currency pair, e.g \"AUDJPY\"

        returns the corresponding CurrencyPair
        """
        nchars = len(name)
        if nchars == 6:
            return cls.from_str_pair(name[0:3], name[3:])
        elif nchars == 7:
            return cls.from_delimited_str(name)
        else:
            raise ValueError("Syntax not recognized for currency pair", name)

    @classmethod
    def from_delimited_str(cls, name: str) -> Self:
        """
        Return the CurrencyPair for a delimited name

        name: a delimited currency pair name, e.g
        `"AUD_USD"` or `"CHF/JPY"`.

        This function will accept any delimiter character
        for the currency pair.

        returns the corresponding CurrencyPair
        """
        if __debug__:
            if len(name) != 7:
                raise AssertionError("Unsupported syntax for a aelimited currency pair", name)
        return cls.from_str_pair(name[0:3], name[4:])

    @classmethod
    def get(cls, name: str):
        """Return a CurrencyPair for a provided currency pair name.

        The `name` string should be provided with the syntax of
        either a concatenated currency pair name, e.g `"CHFJPY"`
        or a delimited currency pair name, e.g `"AUD_USD"`
        """
        if __debug__:
            if not isinstance(name, str):
                raise AssertionError("not a currency pair name", name)
        return cls.from_str(name) if len(name) == 6 else cls.from_delimited_str(name)

    _missing_value_: ClassVar[Callable[[int], Self]] = from_int
    _missing_name_: ClassVar[Callable[[str], Self]] = from_str

    def __index__(self) -> int:
        return self.value

    def __lt__(self, other) -> Union[bool, NotImplementedType]:
        if self.__class__ is other.__class__:
            return self.value < other.value
        else:
            return NotImplemented

    def __gt__(self, other) -> Union[bool, NotImplementedType]:
        if self.__class__ is other.__class__:
            return self.value > other.value
        else:
            return NotImplemented

    def __eq__(self, other) -> Union[bool, NotImplementedType]:
        if id(self) is id(other):
            return True
        elif self.__class__ is other.__class__:
            return self.value == other.value
        else:
            return NotImplemented

    def __str__(self) -> str:
        return self.api_name

    def __bytes__(self) -> bytes:
        return self.api_bytes

    def __hash__(self) -> int:
        if hasattr(self, "_hash_code"):
            return self._hash_code
        else:
            h = hash(self.value)
            self._hash_code = h
            return h

    def __repr__(self) -> str:
        if hasattr(self, "_repr"):
            return self._repr  # type: ignore[has-type]
        else:
            base_digits = self.base_digits
            quote_digits = self.quote_digits
            repr = "<%s.%s [%03d %03d]>" % (self.__class__.__name__, self.name, base_digits, quote_digits)
            self._repr = repr
            return repr


__all__ = ("CurrencyPair",)
