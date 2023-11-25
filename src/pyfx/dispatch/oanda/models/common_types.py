"""Commmon interface types for the fxTrade v20 API"""

from datetime import datetime
from json import JSONEncoder
from numpy import double
from typing import Literal, Optional, Self, Union, TYPE_CHECKING
from typing_extensions import ClassVar

from ..util.naming import exporting
from ..mapped_enum import MappedEnum

from ..transport.transport_base import (
    TransportFloatStr, TransportFloatStrType,
    TransportIntStr, TransportIntStrType,
    TransportEnum, TransportEnumStrType,
    TransportStr, TransportStrType,
    TransportSecretStr, TransportSecretStrType,
    TransportTimestamp, TransportTimestampType
)
from ..credential import Credential
from .currency_pair import CurrencyPair


# must use 'double' type, not 'float' here, or the values
# would be converted fron np.double to 'float' type
# during enum initialization. This would then lead to
# errors during Pydantic field validation, for some values
# of fields using transport types that translate to values
# from this enum class, e.g TransportDecimalAllNone
class DoubleConstants(double, MappedEnum):
    """Enum class for numpy.double (float) constants"""

    __finalize__: ClassVar[Literal[True]] = True

    INF = double("inf")
    NAN = double("nan")
    ZERO = double(0.0)


class AccountId(Credential, TransportSecretStr, metaclass=TransportSecretStrType):
    """
    Account identifier credential for the fxTrade v20 API

    Transport encoding: String
    Runtime encoding: Credential
    """

    storage_class: ClassVar[type] = Credential
    storage_type: ClassVar[type] = Credential
    hash_code: int

    @classmethod
    def create_deferred(cls) -> Self:
        return cls('')

    def deferred(self) -> bool:
        return len(self._secret_value) == 0 if hasattr(self, "_secret_value") else True

    def __repr__(self) -> str:
        if self.deferred() and not self.shadowed():
            return self.__class__.__name__ + "(<deferred>)"
        else:
            return super().__repr__()


class InstrumentName(str, TransportEnum[CurrencyPair, str], metaclass=TransportEnumStrType):
    """
    Symbol name for an instrument in the fxTrade v20 API

    Values for this type will be of a syntax `BBB_QQQ`, for
    `BBB` representing the base currency of the instrument,
    `QQQ` indicating the quote currency, alternately the
    domestic currency of the instrument.

    Each component of the instrument name will be encoded
    as an ISO 4217 three-letter code.

    Transport encoding: String
    Runtime encoding: CurrencyPair (enum)
    """
    storage_class = CurrencyPair
    storage_type = CurrencyPair

    if TYPE_CHECKING:
        name: str
        value: CurrencyPair

    def __new__(cls, arg: Union[CurrencyPair, str]):
        """Return a CurrencyPair for the provided arg"""
        if isinstance(arg, str):
            return CurrencyPair.get(arg)
        else:
            if __debug__:
                if not isinstance(arg, CurrencyPair):
                    raise AssertionError("Not a CurrencyPair", arg)
            return arg

    @classmethod
    def get_display_string(cls, value: CurrencyPair) -> str:
        return value.name

    @classmethod
    def parse(cls, serialized: Union[str, int, CurrencyPair]) -> CurrencyPair:
        if isinstance(serialized, CurrencyPair):
            return serialized
        elif isinstance(serialized, int):
            ## not presented in the v20 API, may be used within other environments:
            ## shifted unsigned integer representation of a currency pair
            return CurrencyPair.from_int(serialized)
        else:
            if __debug__:
                if not isinstance(serialized, str):
                    raise AssertionError("Value is not a string or int", serialized)
            return CurrencyPair.from_str(serialized)

    @classmethod
    def unparse_py(cls, venum: Union[CurrencyPair, int, str], encoder: Optional[JSONEncoder] = None) -> str:
        if isinstance(venum, CurrencyPair):
            return venum.api_name
        elif isinstance(venum, str):
            return '"' + CurrencyPair.from_str(venum).api_name  + '"'
        elif isinstance(venum, int):
            return '"' + CurrencyPair.from_int(venum).api_name + '"'
        else:
            raise ValueError("Not a known CurrencyPair representation ", venum)

    @classmethod
    def unparse_bytes(cls, value: CurrencyPair) -> bytes:
        return b'"' + value.api_bytes + b'"'

    @classmethod
    def unparse_url_bytes(cls, value: Union[CurrencyPair, str]) -> bytes:
        return cls.unparse_bytes(value)

    @classmethod
    def unparse_url_str(cls, value: Union[CurrencyPair, str]) -> bytes:
        return cls.unparse_py(value)


class ClientRequestId(str, TransportStr, metaclass=TransportStrType):
    """
    Request identifier provided by the client

    Transport encoding: String
    Runtime encoding: String
    """


class ClientId(str, TransportStr, metaclass=TransportStrType):
    """
    Client-provided identifier, generally used by
    third party trade platforms in relation to an
    order or trade.

    Transport encoding: String
    Runtime encoding: String
    """


class AccountUnits(double, TransportFloatStr, metaclass=TransportFloatStrType):
    """
    a numeric value representing a quantity of an
    Account's home currency.

    Transport encoding: String-encoded Decimal
    Runtime encoding: numpy.double
    """
    @classmethod
    def get_display_string(cls, value: double) -> str:
        return "{0:.2f}".format(value)


class FloatValue(double, TransportFloatStr, metaclass=TransportFloatStrType):
    """
    an unscoped decimal measure

    Transport encoding: String-encoded Decimal
    Runtime encoding: numpy.double
    """


class PriceValue(double, TransportFloatStr, metaclass=TransportFloatStrType):
    """
    a numeric value representing a unit of price within
    the scope of a defining trade instrument.

    Transport encoding: String-encoded Decimal
    Runtime encoding: numpy.double
    Interface type: float
    """


class LotsValue(double, TransportFloatStr, metaclass=TransportFloatStrType):
    """
    a numeric value representing a quanity of trade units

    This value represents a measure of units, colloquially
    lots or pips within the scope of a defining trade instrument.

    Transport encoding: String-encoded Decimal
    Runtime encoding: numpy.double
    """


class TradeId(int, TransportIntStr, metaclass=TransportIntStrType):
    """
    Trade identifier for the fxTrade v20 API

    Transport encoding: String
    Runtime encoding: Integer
    """


class TransactionId(int, TransportIntStr, metaclass=TransportIntStrType):
    """
    Transaction identifier for the fxTrade v20 API

    Transport encoding: String
    Runtime encoding: Integer
    """
    pass


class OrderId(int, TransportIntStr, metaclass=TransportIntStrType):
    """
    Order identifier

    Transport encoding: String
    Runtime encoding: Integer
    """
    pass


class Time(datetime, TransportTimestamp, metaclass=TransportTimestampType):
    """Timestamp transport type

    Typical Time values in fxapi will be encoded as pd.Timestamp.
    These values will be type-compatible with datetime.datetime

    Transport encoding: String
    Runtime encoding: pd.Timestamp
    Interface type: datetime
    """

__all__ = tuple(frozenset(exporting(__name__, ...)) | {"DoubleConstants"})
