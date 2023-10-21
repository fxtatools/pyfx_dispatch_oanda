## transport type definitions

from enum import Enum
from json import JSONEncoder
from datetime import datetime
from numbers import Real
import numpy as np
import pandas as pd
from pydantic import SecretStr

from types import NoneType
from typing import Literal, Optional, Union
from typing_extensions import ClassVar, Generic, TypeVar

from .transport_base import TransportType, To

from ..util.naming import exporting


class TransportNone(TransportType[None, None]):

    # this assumes a convention of parsing JSON null as None,
    # conversely encoding None as JSON null within the input
    # or output processor. Thus, the value None is used both
    # internally and for the intemediate representaion

    @classmethod
    def parse(cls, unparsed: None) -> None:
        return unparsed

    @classmethod
    def unparse(cls, value: None, encoder: JSONEncoder) -> None:
        return value


class TransportBool(TransportType[bool, str]):
    literal_true: ClassVar[str] = "true"
    literal_false: ClassVar[str] = "false"

    @classmethod
    def unparse(cls, value: bool,
                encoder: Optional[JSONEncoder] = None) -> str:
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
    ## Caveats:
    ## - the fxTrade v20 API uses a quoted string encoding for non-integer
    ##   decimal values (no JSON float encoding)
    ## - NaN values are not supported in the fxTrade v20 API. Although supported
    ##   for internal storage and accepted by the parse() method here, NaN values
    ##   should not be serialized
    @classmethod
    def parse(cls, value: Union[str, Real]) -> np.double:
        if isinstance(value, np.double):
            return value
        else:
            return np.double(value)

    @classmethod
    def unparse(cls, value: np.double, encoder: Optional[JSONEncoder] = None) -> str:
        if __debug__:
            if value == np.nan:
                raise AssertionError("Not serializable for transport", value)
        return str(value)


class TransportInt(TransportType[int, int]):
    ## assumption: The server will encode int value as int,
    ## without quoting on the transport values
    @classmethod
    def unparse(cls, value: int,
                encoder: Optional[JSONEncoder] = None) -> int:
        return value

    @classmethod
    def parse(cls, value: int) -> int:
        return value


class TransportIntStr(TransportType[int, str]):
    ## the server may encode some integer identifiers as string values
    ## e.g TradeID
    @classmethod
    def unparse(cls, value: int,
                encoder: Optional[JSONEncoder] = None) -> str:
        return str(value)

    @classmethod
    def parse(cls, value: str) -> int:
        return int(value)


class TransportStr(TransportType[str, str]):
    @classmethod
    def unparse(cls, value: str,
                encoder: Optional[JSONEncoder] = None) -> str:
        return value

    @classmethod
    def parse(cls, value: str) -> str:
        return value


class TransportSecretStr(TransportType[SecretStr, str]):
    @classmethod
    def unparse(cls, value: SecretStr,
                encoder: Optional[JSONEncoder] = None) -> str:
        return value.get_secret_value()

    @classmethod
    def parse(cls, value: str) -> SecretStr:
        return SecretStr(value)


class TransportTimestamp(TransportType[datetime, str]):
    """Nullable datetime transport type

    Storage Type: Union[pd.Timestamp, Literal[pd.NaT]]
    Storage Class: datetime.datetime
    Transport Value Class: str
    """

    ## case study: GetAccountSummary200Response => AccountSummary => resettable_pl_time
    ## - transmitted sometimes as "0".
    ## - when present in the response, the resettable_pl_time must be parsed nonetheless
    ## - when parsed as a timestamp string, the usage of "0" may lead to unexpected data
    ##   in deserialization
    ##

    storage_class = pd.Timestamp

    @classmethod
    def unparse(cls, value: datetime,
                encoder: Optional[JSONEncoder] = None) -> str:
        if value == pd.NaT:
            return "0"
        else:
            return value.isoformat()

    @classmethod
    def parse(cls, dt: Union[str, datetime]) -> datetime:
        if isinstance(dt, pd.Timestamp):
            return dt
        elif isinstance(dt, datetime):
            return pd.to_datetime(dt)
        else:
            if __debug__:
                if not isinstance(dt, str):
                    raise AssertionError("Not a string", dt)
            dtlen = len(dt)
            if dtlen is int(1):
                if __debug__:
                    if dt != "0":
                        raise AssertionError("Unrecognized value", dt)
                return pd.NaT
            else:
                try:
                    ## assumption: ISO format
                    return pd.to_datetime(dt, unit='ns')
                except:
                    ## assumption: Epoch format
                    try:
                        return pd.to_datetime(float(dt), unit='s')
                    except:
                        return pd.NaT

Tenum = TypeVar("Tenum", bound=Enum)


class TransportEnum(TransportType[Tenum, To]):

    @classmethod
    def parse(cls, serialized: To) -> Union[Tenum, To]:  # type: ignore
        storage_cls: type[Enum] = cls.storage_class
        map = storage_cls._member_map_
        if serialized in map:
            return map[serialized]  # type: ignore
        else:
            return serialized

    @classmethod
    def unparse(cls, venum: Tenum,
                encoder: Optional[JSONEncoder] = None) -> To:
        return venum.value


class TransportEnumString(TransportEnum[Tenum, str], Generic[Tenum]):
    pass


class TransportEnumInt(TransportEnum[Tenum, int], Generic[Tenum]):
    pass


__all__ = tuple(frozenset(exporting(__name__, ..., Tenum)))
