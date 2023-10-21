"""Commmon interface types for the fxTrade v20 API"""

from datetime import datetime
from json import JSONEncoder
from numpy import double
from enum import Enum
# from pandas import NaT

from typing_extensions import TypeAlias

from ..util.naming import exporting

from ..transport.transport_base import TransportType
from ..transport.transport_types import TransportIntStr, TransportFloatStr, TransportStr
from ..credential import Credential


class DoubleConstants(double, Enum):
    INF = double("inf")
    NAN = double("nan")
    ZERO = double(0.0)


class TransportCredential(TransportType[Credential, str]):
    @classmethod
    def unparse(cls, value: Credential, encoder: JSONEncoder) -> str:
        return value.get_secret_value()


class AccountId(Credential, metaclass=TransportCredential):
    """
    Account identifier credential for the fxTrade v20 API

    Transport encoding: String
    Runtime encoding: Credential
    """


class InstrumentName(str, metaclass=TransportStr):  # type: ignore
    """
    Symbol name for an instrument in the fxTrade v20 API

    Values for this type will be of a syntax `BBB_QQQ`, for
    `BBB` representing the base currency of the instrument,
    `QQQ` indicating the quote currency, alternately the
    domestic currency of the instrument.

    Each component of the instrument name will be encoded
    as an ISO 4217 three-letter code.

    Transport encoding: String
    Runtime encoding: String
    """


class ClientRequestId(str, metaclass=TransportStr):  # type: ignore
    """
    Request identifier provided by the client

    Transport encoding: String
    Runtime encoding: String
    """


class ClientId(str, metaclass=TransportStr):  # type: ignore
    """
    Client-provided identifier, generally used by
    third party trade platforms in relation to an
    order or trade.

    Transport encoding: String
    Runtime encoding: String
    """


class AccountUnits(double, metaclass=TransportFloatStr):
    """
    a numeric value representing a quantity of an
    Account's home currency.

    Transport encoding: String-encoded Decimal
    Runtime encoding: numpy.double
    """


class FloatValue(double, metaclass=TransportFloatStr):
    """
    an unscoped decimal measure

    Transport encoding: String-encoded Decimal
    Runtime encoding: numpy.double
    """


class PriceValue(double, metaclass=TransportFloatStr):
    """
    a numeric value representing a unit of price within
    the scope of a defining trade instrument.

    Transport encoding: String-encoded Decimal
    Runtime encoding: numpy.double
    """


class LotsValue(double, metaclass=TransportFloatStr):
    """
    a numeric value representing a quanity of trade units

    This value represents a measure units, lots or pips
    within the scope of a defining trade instrument.

    Transport encoding: String-encoded Decimal
    Runtime encoding: numpy.double
    """


class TradeId(int, metaclass=TransportIntStr):
    """
    Trade identifier for the fxTrade v20 API

    Transport encoding: String
    Runtime encoding: Integer
    """


class TransactionId(int, metaclass=TransportIntStr):
    """
    Transaction identifier for the fxTrade v20 API

    Transport encoding: String
    Runtime encoding: Integer
    """
    pass


class OrderId(int, metaclass=TransportIntStr):
    """
    Order identifier

    Transport encoding: String
    Runtime encoding: Integer
    """
    pass


Time: TypeAlias = datetime
"""Time storage alias.

Typical Time values in fxapi will be encoded as pd.Timestamp.
These values will be type-compatible with datetime.datetime
"""


__all__ = tuple(exporting(__name__, ..., "Time"))
