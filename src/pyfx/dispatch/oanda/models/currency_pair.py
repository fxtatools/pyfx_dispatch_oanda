"""Currency Pair encoding for applications"""

from typing import Self

from aenum import Enum, extend_enum

from .currency import Currency

CURRENCY_PAIR_BASE_SHIFT: int = 16
CURRENCY_PAIR_QUOTE_MASK: int = 0xffff


class CurrencyPair(Enum):
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

    @property
    def base_digits(self) -> int:
        """ISO 4217 numerical code representing the base currency"""
        if hasattr(self, "_base_currency"):
            return self._base_currency.digits
        else:
            return self.value >> CURRENCY_PAIR_BASE_SHIFT

    @property
    def quote_digits(self) -> int:
        """ISO 4217 numerical code representing the quote currency"""
        if hasattr(self, "_quote_currency"):
            return self._quote_currency.digits
        else:
            return self.value & CURRENCY_PAIR_QUOTE_MASK

    @property
    def base_currency(self) -> Currency:
        """Currency enum member representing the base currency"""
        if hasattr(self, "_base_currency"):
            return self._base_currency
        else:
            base_digits = self.base_digits
            base = Currency.from_digits(base_digits)
            self._base_currency = base
            return base

    @property
    def quote_currency(self) -> Currency:
        """Currency enum member representing the quote currency"""
        if hasattr(self, "_quote_currency"):
            return self._quote_currency
        else:
            quote_digits = self.quote_digits
            quote = Currency.from_digits(quote_digits)
            self._quote_currency = quote
            return quote

    @classmethod
    def from_str_pair(cls, base: str, quote: str) -> Self:
        """Return the CurrencyPair for a set of base and quote currency symbols
        
        base: ISO 4217 three-digit alphabetical code for the base currency
        quote: ISO 4217 three-digit alphabetical code for the quote currency

        returns the corresponding CurrencyPair
        """
        base_cur = Currency.from_alpha(base)
        quote_cur = Currency.from_alpha(quote)
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
            return inst

    @classmethod
    def from_int(cls, code: int) -> Self:
        """
        Return the CurrencyPair for a CurrencyPair integer code

        code: a CurrencyPair integer code.

        returns the corresponding CurrencyPair
        """
        codes_map = cls._value2member_map_
        if code in codes_map:
            return codes_map[code]
        else:
            base_cur = Currency.from_digits(code >> CURRENCY_PAIR_BASE_SHIFT)
            quote_cur = Currency.from_digits(code & CURRENCY_PAIR_QUOTE_MASK)
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
        return cls.from_str_pair(name[0:3], name[3:])

    @classmethod
    def from_delimited_str(cls, name: str) -> Self:
        """
        Return the CurrencyPair for a delimited name

        name: a delimited currency pair, e.g \"AUD_USD\" or \"CHF/JPY\"

        returns the corresponding CurrencyPair
        """
        return cls.from_str_pair(name[0:3], name[4:])

    def __index__(self) -> int:
        return self.value

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        if hasattr(self, "_repr"):
            return self._repr
        else:
            base_digits = self.base_digits
            quote_digits = self.quote_digits
            repr = "<%s.%s [%d %d]>" % (self.__class__.__name__, self.name, base_digits, quote_digits)
            self._repr = repr
            return repr


__all__ = ("CurrencyPair",)
