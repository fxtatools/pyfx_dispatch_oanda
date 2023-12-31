"""Currency defininition for applications"""

from aenum import extend_enum
from currency_symbols import CurrencySymbols  # type: ignore[import-untyped]
from json import JSONEncoder
from numpy import ushort
from immutables import Map
from typing import Literal, Union
from typing_extensions import ClassVar, Self
import isocodes


from ..mapped_enum import MappedEnum

from ..transport.data import JsonTypesRepository
from ..transport.transport_base import TransportEnumStrType

CURRENCY_ALPHA_DIGITS: Map[str, ushort] = Map(
    (cur['alpha_3'], ushort(cur['numeric']),) for cur in isocodes.currencies.items
)

CURRENCY_DIGITS_ALPHA: Map[ushort, str] = Map(
    (CURRENCY_ALPHA_DIGITS[cur['alpha_3']], cur['alpha_3'],) for cur in isocodes.currencies.items
)

CURRENCY_DIGITS_NAMES: Map[str, str] = Map(
    (CURRENCY_ALPHA_DIGITS[datum['alpha_3']], datum['name'],)for datum in isocodes.currencies.items  # type: ignore[misc]
)

class Currency(int, MappedEnum):
    """
    Currency identifier (ISO 4217 coding, with extensions)

    **Overview**

    Enum members in the Currency class are derived primarily from the `isocodes.currency`
    table, with currency symbol information provided from `currency_symbols`. Additional
    coding is provided as denoted, below, under "Extensions"

    **Implementation and Usage**

    Each Currency enum member is indexed with an enum member name representing a three
    character alphabetical code. Where applicable, this code denotes the ISO 4217
    three character alphabeitcal code for the representative currency. This alphabetical
    code may be accessed with either of the properties `name` or indirectly as `alpha`
    for the Currency enum member.

    The ISO 4217 three-digit numerical code for a Currency may be accessed as a numpy.ushort
    value, using with the `value` property on the Enum member, or indirectly via the `digits`
    property. For alphabetical currency codes not recognized  under ISO 4217, the digit encoding
    is described under "Extensions,"  below.


    The currency's single-character significant symbol may be accessed with the `symbol` property.

    Currency enum members can be located using the method `Currency.get(ident)`, given  an `ident`
    value providing either a  three character alphabetical code or as an integer value representing
    the thee digit numerical code of a currency as presented under ISO 4217.

    Currency Enum members can also be located with the conventional subscript notation, e.g
    `Currency[<ALPHA>]` or `Currency[<DIGITS_INT>]`

    ```python
    >>> from pyfx.dispatch.oanda.models.currency import Currency

    >>> Currency.get('AUD')
    <Currency.AUD: 036>

    >>> Currency.get(36)
    <Currency.AUD: 036>

    >>> Currency.get(36) is Currency.get('AUD')
    True
    ```

    **Extensions**

    The currency code "CNH", though commonly used in financial systems, is not recognized as a
    currency code under ISO 4217.

    For purpose of consistent numerical encoding, "CNH" is represented here with an integer
    encoding of the ordinal value of characters in the string "CNH", literally the value 0x47e8

    **Property accessors**

    - Currency.name -> str
    - Currency.value -> numpy.ushort
    - Currency.alpha -> str
    - Currency.digits-> numpy.ushort
    - Currency.digits_str -> str
    - Currency.symbol -> str
    - Currency.description -> str

    **Class methods**

    - Currency.get(ident: Union[int, str]) -> Currency

    """

    def __str__(self) -> str:
        return self.name

    def __bytes__(self) -> bytes:
        if hasattr(self, "_bytes"):
            return self._bytes   # type: ignore[has-type]
        else:
            bstr = self.name.encode()
            self._bytes = bstr
            return bstr

    def __repr__(self) -> str:
        if hasattr(self, "_repr"):
            return self._repr  # type: ignore[has-type]
        else:
            repr = "<{0:s}.{1:s}: {2:03d}>".format(self.__class__.__name__, self.name, self.value)
            self._repr = repr
            return repr

    @property
    def alpha(self) -> str:
        """
        Return the ISO 4217 three letter alphabetical code for the representative currency.

        This value may be accessed directly via the `name` property of each enum member.
        """
        return self.name

    @property
    def digits(self) -> ushort:
        """Return an numpy.ushort value denoting the ISO 4217 three digit numerical code
        for the  representative currency.

        This value may be accessed directly via the `value` property of each enum member.
        """
        return self.value

    @property
    def digits_str(self) -> str:
        """Return a string denoting the ISO 4217 three digit numerical code for the
        representative currency. This string will include any leading digits comprising
        the numerical code, as a string value.
        """
        if hasattr(self, "_digits_str"):
            return self._digits_str  # type: ignore[has-type]
        else:
            s = "{0:03d}".format(self.value)
            self._digits_str = s
            return s

    @property
    def symbol(self) -> str:
        """Return a string denoting the representaive symbol for this currency

        This property is not defined in ISO 4217
        """
        if hasattr(self, "_symbol"):
            return self._symbol  # type: ignore[has-type]
        else:
            s = CurrencySymbols.get_symbol(self.name)
            self._symbol = s
            return s

    @property
    def description(self) -> str:
        """
        Return a descriptive name (EN) for the representative currency.

        This property's value is cached dynamically from the `isocodes.currency` table, on first access for each enum member.
        """
        if hasattr(self, "_description"):
            return self._description  # type: ignore[has-type]
        else:
            desc = CURRENCY_DIGITS_NAMES[self.value]
            self._description = desc
            return desc

    def __index__(self) -> int:
        """Return the numerical code for this Currency enumber member, as an unsigned short value"""
        return self.value

    @classmethod
    def get(cls, ident: Union[int, str]) -> Self:
        # Implementation note: If ident does not denote a known currency name,
        # then a new currency enum object will be created with a non-standard
        # integer code derived from a bitwise shift of each byte in the byte
        # encoding for characters in the name.
        #
        # While this API assumes an unsighed 32-bit numeric encoding for the
        # integer part of a currency symbol, it is possible that the numeric
        # encoding for a user-provided string might exceed this bitwise bound.
        # (The bound is not checked here, but it would be trivial to implement
        #  an assertion for this. FIXME)
        #
        # The market symbol "CNH" will typically have been preloaded under
        # .currency_pair

        if isinstance(ident, str):
            try:
                return cls._member_map_[ident]
            except KeyError:
                if cls.__finalized__:
                    raise RuntimeError("Currency name not supported", ident)
                else:
                    ccode = cls.ccode(ident)
                    return extend_enum(cls, ident, ccode)
        elif isinstance(ident, int):
            return cls._value2member_map_[ident]
        else:
            raise ValueError("Unrecognized currency identifier", ident)

    @staticmethod
    def ccode(ident: str) -> int:
        ct = len(ident)
        n = 0
        for (off, c) in enumerate(ident[::-1]):
            n |= (ord(c) << off * 4)
        return n

    __gen__ = ((dct["alpha_3"], ushort(dct["numeric"]),)
               for dct in isocodes.currencies.items.copy() + [
                   dict(alpha_3 = "CNH", numeric=str(ccode("CNH")))
                   ])

    ## if freezing the enum, thus making the member map
    ## an immutable map, it would not permit adding any
    ## "new" currency symbols such that may not have
    ## been indexed in the orignial API
    ##
    # __finalize__: ClassVar[Literal[True]] = True



class TransportCurrencyKind(TransportEnumStrType[Currency, str]):
    @classmethod
    def unparse_py(cls, venum: Currency, encoder: JSONEncoder) -> str:
        return venum.alpha


JsonTypesRepository.bind_transport_type(Currency, TransportCurrencyKind)


__all__ = ("Currency",)
