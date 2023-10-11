## transport type definitions

from enum import Enum
from json import JSONEncoder
from numbers import Real
import numpy as np
import pandas as pd
from pydantic import SecretStr

from types import NoneType
from typing import Union
from typing_extensions import ClassVar, Generic, TypeVar

from .transport_base import TransportType, To

from ..util.naming import exporting


class TransportNone(TransportType[NoneType, NoneType]):

    # this assumes a convention of parsing JSON null as None,
    # conversely encoding None as JSON null within the input
    # or output processor. Thus, the value None is used both
    # internally and for the intemediate representaion

    @classmethod
    def parse(cls, unparsed: NoneType) -> NoneType:
        return unparsed

    @classmethod
    def unparse(cls, value: NoneType, encoder: JSONEncoder) -> NoneType:
        return value


class TransportBool(TransportType[bool, str]):
    literal_true: ClassVar[str] = "true"
    literal_false: ClassVar[str] = "false"

    @classmethod
    def unparse(cls, value: bool,
                encoder: JSONEncoder) -> str:
        if value is True:
            return cls.literal_true
        elif value is False:
            return cls.literal_false
        else:
            raise ValueError("Non-boolean output value", value)

    @classmethod
    def parse(cls, value: Union[bool, str]) -> bool:
        # during processing for an abstract API model type,
        # parse() may receive a parsed boolean value
        if value == cls.literal_true or value is True:
            return True
        elif value == cls.literal_false or value is False:
            return False
        else:
            raise ValueError("Non-boolean input value", value)


class TransportFloatStr(TransportType[np.double, str]):
    ## the v20 fxTrade API uses a quoted string encoding for decimal values,
    ## rather than an unquoted JSON float encoding, throughout the API.
    @classmethod
    def parse(cls, value: Union[str, Real]) -> float:
        return np.double(value)

    @classmethod
    def unparse(cls, value: np.double, encoder: JSONEncoder) -> str:
        return str(value)


class TransportInt(TransportType[int, int]):
    ## assumption: The server will encode int value as int,
    ## without quoting on the transport values
    @classmethod
    def unparse(cls, value: int,
                encoder: JSONEncoder) -> int:
        return value

    @classmethod
    def parse(cls, value: int) -> int:
        return value


class TransportIntStr(TransportType[int, str]):
    ## the server may encode some integer identifiers as string values
    ## e.g TradeID
    @classmethod
    def unparse(cls, value: int,
                encoder: JSONEncoder) -> str:
        return str(value)

    @classmethod
    def parse(cls, value: str) -> int:
        return int(value)


class TransportStr(TransportType[str, str]):
    @classmethod
    def unparse(cls, value: str,
                encoder: JSONEncoder) -> str:
        return value

    @classmethod
    def parse(cls, value: str) -> str:
        return value


class TransportSecretStr(TransportType[SecretStr, str]):
    @classmethod
    def unparse(cls, value: SecretStr,
                encoder: JSONEncoder) -> str:
        return value.get_secret_value()

    @classmethod
    def parse(cls, value: str) -> SecretStr:
        return SecretStr(value)


class TransportTimestamp(TransportType[pd.Timestamp, str]):
    @classmethod
    def unparse(cls, value: pd.Timestamp,
                encoder: JSONEncoder) -> str:
        return value.isoformat()

    @classmethod
    def parse(cls, dtstr: str) -> pd.Timestamp:
        try:
            ## assumption: ISO format
            return pd.to_datetime(dtstr, unit='ns')
        except:
            ## assumption: Epoch format
            return pd.to_datetime(float(dtstr), unit='s')


Tenum = TypeVar("Tenum", bound=Enum)


class TransportEnum(TransportType[Tenum, To], Generic[Tenum, To]):

    @classmethod
    def parse(cls, serialized: To) -> Union[Tenum, To]:
        storage_cls: type[Enum] = cls.storage_class
        map = storage_cls._member_map_
        if serialized in map:
            return map[serialized]
        else:
            return serialized

    @classmethod
    def unparse(cls, venum: Tenum,
                encoder: JSONEncoder) -> To:
        return venum.value


class TransportEnumString(TransportEnum[Tenum, str], Generic[Tenum]):
    pass


class TransportEnumInt(TransportEnum[Tenum, int], Generic[Tenum]):
    pass


__all__ = tuple(frozenset(exporting(__name__, ..., Tenum)))
