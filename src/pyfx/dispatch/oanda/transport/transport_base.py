## base types for transport type, transport field definitions

from abc import ABC, ABCMeta
from collections.abc import Sequence
from datetime import datetime

from .application_fields import ApplicationFieldInfo
from ..mapped_enum import MappedEnum
from enum import Enum
from json import JSONEncoder
import logging
from numbers import Real
from typing import Any, Generic, Optional, Union
from typing_extensions import ClassVar, TypeAlias, Self, TypeVar, get_args, get_origin, get_original_bases
import numpy as np
import pandas as pd
from urllib.parse import quote_from_bytes

from pydantic import SecretStr

from ..util.typeref import get_type_class, TypeRef
from ..util.naming import exporting

from .encoder_constants import EncoderConstants


Ti = TypeVar("Ti")
To = TypeVar("To")

InitArg = TypeVar("InitArg")

logger = logging.getLogger(__name__)


def get_sequence_member_class(spec: TypeRef) -> type:
    """Utility function for initialization of values transport types

    Provided with a type specifier `spec`, generally as a type alias
    with a syntax such  as `Optional[List[<cls>>]]`, returns the <cls>
    dentoed in the type alias.
    """
    # if __debug__:
    #     if not isinstance(spec, GenericAlias):
    #         raise AssertionError("Not a generic alias type specifier", spec)
    origin = get_origin(spec)
    if origin == Union:
        ## parse a stored type alias from an Optional[concrete_type] declaration
        args = get_args(spec)
        if args and len(args) is int(2) and args[-1] == None.__class__:
            return get_sequence_member_class(args[0])
        else:
            ## too many type names in the Union type
            raise ValueError("Unable to determine a concrete class for type declaration", spec)
    elif not issubclass(origin, Sequence):
        raise ValueError("Not a sequence type specifier", spec)
    args = get_args(spec)
    if args and len(args) is int(1):
        return get_type_class(args[0])
    else:
        raise ValueError("Unable to determine a concrete member class for sequence type declaration", spec)



class TransportInterfaceClass(ABCMeta):
    def __subclasscheck__(cls, test_cls: type) -> bool:
        """Abstract subclass check for TransportType type instance scope

        subcls: A class to test for subclass relation to this TransportType class

        Returns true if the TypeClass `cls` is in the MRO for `test_cls`
        """
        return cls in test_cls.__mro__
    def __instancecheck__(cls, instance: Any) -> bool:
        """Abstract instance check for TransportType type instance scope

        instance: An object to test for instance relation to this
        TransportType class

        Returns true if TransportType class `cls` is present in the MRO for
        the instance's class, or if `cls` has a defined `storage_class`
        attribute and that `storage_class` is present in the MRO for the
        instance's class.
        """
        if instance == "cls":
            return False
        if isinstance(instance, type):
            return cls in instance.__mro__
        imro = instance.__class__.__mro__
        if cls in imro:
            return True
        elif hasattr(cls, "storage_class") and cls.storage_class in imro:
            return True
        else:
            styp = cls.storage_type if hasattr(cls, "storage_type")  else None
            if styp and isinstance(styp, cls):
                return styp in imro


class TransportInterface(Generic[Ti, To], metaclass=TransportInterfaceClass):

    storage_type: ClassVar[TypeRef]
    """Effective storage type for values of this transport type"""

    storage_class: ClassVar[type]
    """Storage interface class for values of this transport type


    The default `parse()` method will apply this class name as
    a constructor function. The function will be provided with the
    intermediate transport value received by `parse()
    """

    serialization_type: ClassVar[TypeRef]
    """Intermediate serialization type for protocol data encoding

    For a transport type serialized to JSON, this type would typically
    denote the type of value processed by the JSON encoder or decoder.
    """

    serialization_class: ClassVar[type]
    """Intermediate serialization class for protocol data encoding

    For a transport type serialized to JSON, this class would typically
    denote the class of value processed by the JSON encoder or decoder.

    The default `unparse_py()` method will apply this class name as a constructor
    function to the value provided to `unparse+py()`. The object returned by the
    constructor will be passed to the transport encoder provided to `unparse_py()`
    """

    @classmethod
    def check_type(cls, value) -> bool:
        return isinstance(value, cls.storage_class)

    @classmethod
    def unparse_py(cls, value: Ti, encoder: JSONEncoder) -> To:
        """Return a serializable object representing a value
        of this transport type.

        The return value should be produced with a type compatible with
        this transport type's serialization encoding. Structurally, the
        value should have a syntax compatible with the return value of
        `json.JSONEncoder.default()`

        Params:
        value: the value to unparse
        decoder: a JSONEncoder instance.

        Returns: the encoded object, in this transport type's
        serialization encoding
        """

        ## encoder: JSON encoder for structured object deserializtion.
        ##
        ## This default method is applicable for literal serialization
        ## types only
        if not encoder:
            raise AssertionError("No encoder", value)
        return encoder.default(cls.serialization_class(value))

    @classmethod
    def unparse_bytes(cls, value: Ti) -> bytes:
        ## the default implementation assumes that the value will not need further quoting, for form data syntax
        return value if isinstance(value, bytes) else str(value).encode()

    @classmethod
    def unparse_url_bytes(cls, value: Ti) -> bytes:
        ## the default implementation assumes that the value will not need further quoting, for URL syntax
        return value if isinstance(value, bytes) else str(value).encode()

    @classmethod
    def unparse_url_str(cls, value: Ti) -> bytes:
        ## the default implementation assumes that the value will not need further quoting, for URL syntax
        return value if isinstance(value, str) else str(value)

    @classmethod
    def parse(cls, unparsed: To) -> Ti:
        if __debug__:
            if not hasattr(cls, "storage_class"):
                raise AssertionError("No storage_class defined", cls)
        return cls.storage_class(unparsed)

    @classmethod
    def get_display_string(cls, value: Ti) -> str:
        return str(value)

    @classmethod
    def get_state(cls, object):
        ## default method for scalar values
        return object

    @classmethod
    def restore_state(cls, field, m_object, state):
        ## default method for scalar values, where 'state' is the  value itself
        ##
        ## note that this method does not need to affect __pydantic_fields_set__ in the object
        m_object.__dict__[field] = state

    @classmethod
    def restore_member_state(cls, field, m_object, m_value):
        ## scalar values can be stored literally within sequence types and in model state information
        ##
        ## this method is used mainly in TransportValuesType.restore_state(...)
        return m_value

    @classmethod
    def __init_subclass__(cls, *args, **kw):
        # utility function for application after new_class() and within cls.__new__()
        super().__init_subclass__
        cls.initialize_attrs()

    @classmethod
    def initialize_attrs(cls):
        """Initialize attributes of the TransportInterface class"""
        if ABC in cls.__bases__:
            return
        attrs = cls.__dict__
        if hasattr(cls, "storage_class"):
            scls = cls.storage_class
            if scls is Self:
                cls.storage_class = cls
        else:
            for b in cls.__bases__:
                if hasattr(b, "storage_class"):
                    cls.storage_class = b.storage_class
                    break
        if hasattr(cls, "storage_type"):
            styp = cls.storage_type
            if styp is Self:
                cls.storage_type = cls
        else:
            for b in cls.__bases__:
                if hasattr(b, "storage_type"):
                    cls.storage_type = b.storage_type
                    break


        ## if the class definition does not already provide type/class information
        ## for storage values and/or transport (serialization) values, derive the
        ## transport storage and serialization classes for the class, based on args
        ## provided to a TransportInterface generic type, if provided as a base class
        ## of the cls
        for gen_base in get_original_bases(cls):
            origin = get_origin(gen_base)
            if origin and issubclass(origin, TransportInterface):
                args = get_args(gen_base)
                if len(args) is not int(2):
                    continue
                ityp = args[0]
                if not isinstance(ityp, TypeVar):
                    if 'storage_type' not in attrs:
                        cls.storage_type = ityp
                    if 'storage_class' not in attrs:
                        icls = get_type_class(ityp)
                        cls.storage_class = get_type_class(ityp)
                otyp = args[1]
                if not isinstance(otyp, TypeVar):
                    if "serialization_type" not in attrs:
                        cls.serialization_type = otyp
                    if "serialization_class" not in attrs:
                        cls.serialization_class = get_type_class(otyp)
                break


class TransportObject(TransportInterface[Ti, To]):
    def __new__(cls, arg: Union[Ti, To]) -> Self:
        return cls.parse(arg)


T_co = TypeVar("T_co", covariant=True)


class TransportTypeClass(TransportInterfaceClass, ABCMeta, type[T_co]):

    def __subclasscheck__(cls, test_cls: type) -> bool:
        """support for `__subclasscheck__` at the TransportType type instance scope

        Returns True if the type metaclass `cls` is in the MRO for the type `test_cls`
        """
        return cls in test_cls.__mro__

    def __instancecheck__(cls, instance: Any) -> bool:
        """support for `__instancecheck__` at the TransportType type instance scope

        Returns True if type metaclass `cls` is in the MRO for the `__class__` of the instance
        """
        return cls in instance.__class__.__mro__


class TransportType(type, TransportInterface[Ti, To], metaclass=TransportTypeClass):
    # base class for TransportInterface classes defininig a type class
    pass

class TransportFieldInfo(ApplicationFieldInfo, Generic[Ti, To]):
    '''FieldInfo base class for transport fields'''

    __slots__ = tuple(list(ApplicationFieldInfo.__slots__) + [
        "transport_type", "value_type",
        "json_name", "json_name_bytes",
        "storage_class", "deprecated"
    ])

    transport_type: TransportType[Ti, To]
    value_type: Union[type, TypeRef]
    json_name: str
    json_name_bytes: bytes
    storage_class: type
    deprecated: bool

    def __init__(self, default, transport_type: TransportType[Ti, To], deprecated=None, **kw):
        # Implementation note: Processing for TransportTypeInfer
        #
        # For each field and field info pair of an ApiObjbect class, the field info's transport
        # type binding will be further processed duirng ApiObject class initialization. This
        # would be mainly to replace any TransportTypeInfer type with a transport type determined
        # from metadata for the field, at the class scope.
        #
        # Once a concrete tranpsort type is determined for the Field Info instance, additional
        # processing may be applied under self.bind()
        self.transport_type = transport_type
        self.deprecated = deprecated
        super().__init__(default=default, **kw)

    @classmethod
    def from_field(cls, default, transport_type: TransportType[Ti, To], **kw):  # type: ignore
        return cls(default, transport_type=transport_type, **kw)

    def bind(self, field_name: str, cls: type):
        """Set addtional metadata for JSON encoding of the field, after ApplicationFieldInfo.bind()

        This method will configure the following field attributes, when no `json_name` attribute
        has been defined in `self`:
        - `json_name` : the first _truthy_ value of the the alias name or field name for the field
        - `json_name_bytes` : bytes encoding for the JSON field name
        """
        super().bind(field_name, cls)
        if not hasattr(self, "json_name"):
            json_name = self.alias or field_name
            self.json_name = json_name
            self.json_name_bytes = json_name.encode()

    def __repr__(self):
        """Return a repr string for this field info object, denoting the field info
        class, field name,  and defining class

        For each of the *defining class* and *field name* atrributes: If the attribute
        has not been set for the field info object, the repr string will include the
        text, `<Undefined>`. as a place holder for that attribute value.
        """
        defining = self.defining_class.__name__ if hasattr(self, "defining_class") else "<Undefined>"
        name = self.name if hasattr(self, "name") else "<Undefined>"
        return "<%s [%s.%s] at 0x%x>" % (self.__class__.__name__, defining, name, id(self),)


class TransportTypeInfer(TransportType[None, None]):
    """Intermediate TransportType class

    For each *field* and *field info* pair within an ApiObject class: If the field
    info object is defined with the class TransportTypeInfer as the transport type
    for the field definition, then the field will be processed during ApiObject
    class initialization as to infer the real transport type for the field. This
    inference would be applied at the class scupe, using field annotations onto the
    transport types repository for the initialized ApiObject class.
    """
    pass


TRANSPORT_VALUES_STORAGE_CLASS: TypeAlias = list
"""Type alias denoting the storage class for internal representation of JSON array values"""


class TransportValuesType(TransportType[TRANSPORT_VALUES_STORAGE_CLASS[Ti], list[To]], Generic[Ti, To]):
    member_transport_type: TransportType[Ti, To]

    @classmethod
    def get_storage_class(cls):
        return TRANSPORT_VALUES_STORAGE_CLASS

    @classmethod
    def parse_member(cls, value: To) -> Ti:
        return cls.member_transport_type.parse(value)

    @classmethod
    def unparse_member(cls, value: Ti, encoder: JSONEncoder) -> To:
        return cls.member_transport_type.unparse_py(value, encoder)

    @classmethod
    def parse(cls, unparsed: list[To]) -> TRANSPORT_VALUES_STORAGE_CLASS[Ti]:
        return [cls.parse_member(elt) for elt in unparsed]

    @classmethod
    def unparse_py(cls, value: list[Ti],
                   encoder: JSONEncoder) -> list[To]:
        return [cls.unparse_member(elt, encoder) for elt in value]

    @classmethod
    def unparse_bytes(cls, value: TRANSPORT_VALUES_STORAGE_CLASS[Ti]) -> bytes:
        mtyp = cls.member_transport_type
        return EncoderConstants.START_ARRAY.value + b','.join(mtyp.unparse_bytes(elt) for elt in value) + EncoderConstants.END_ARRAY.value

    @classmethod
    def unparse_url_bytes(cls, value: TRANSPORT_VALUES_STORAGE_CLASS) -> bytes:
        mtyp = cls.member_transport_type
        return b','.join(mtyp.unparse_url_bytes(elt) for elt in value)

    @classmethod
    def unparse_url_str(cls, value: TRANSPORT_VALUES_STORAGE_CLASS) -> str:
        mtyp = cls.member_transport_type
        return ','.join(mtyp.unparse_url_str(elt) for elt in value)

    @classmethod
    def get_state(cls, object):
        mtyp = cls.member_transport_type
        return tuple(mtyp.get_state(v) for v in object)

    @classmethod
    def restore_state(cls, field, m_object, state):
        # mtyp = cls.member_transport_type
        # return TRANSPORT_VALUES_STORAGE_CLASS(mtyp.restore_state(v) for v in state)
        mtyp = cls.member_transport_type
        value = TRANSPORT_VALUES_STORAGE_CLASS(mtyp.restore_member_state(field, m_object, v) for v in state)
        setattr(m_object, field, value)

    @classmethod
    def restore_member_state(cls, field, m_object, m_value):
        logger.critical("Nested value sequences are not supported in this version of the serialization API: Class %s field %s", m_object.__class__.__name, field)
        ## returning the value, unprocessed - this transport type does not support arbitrary nesting or recursion for member transport types
        return m_value

    @classmethod
    def __init_subclass__(cls, *, member_class=None, **kw):
        if member_class:
            ## if not provided, member_class should be initialized later
            cls.member_transport_type = member_class
        super().__init_subclass__(**kw)


#
# Transport Type Definitions
#


class TransportNone(TransportType[None, None]):

    # this assumes a convention of parsing JSON null as None,
    # conversely encoding None as JSON null within the input
    # or output processor. Thus, the value None is used both
    # internally and for the intemediate representaion


    @classmethod
    def parse(cls, unparsed: None) -> None:
        return unparsed

    @classmethod
    def unparse_py(cls, value: None, encoder: JSONEncoder) -> None:
        return value

    @classmethod
    def unparse_bytes(cls, value: None) -> bytes:
        if __debug__:
            if value is not None:
                raise AssertionError("value is not None", value)
        return b'null'


class TransportNoneType(TransportNone, TransportType[None.__class__, None.__class__]):
    pass


class TransportBool(TransportInterface[bool, bool]):
    storage_class: ClassVar[type[bool]] = bool

    @classmethod
    def parse(cls, value: Union[bool, str]) -> bool:
        # during processing for an abstract API model type,
        # parse() may receive a parsed boolean value
        if value == EncoderConstants.TRUE.str_value or value is True:
            return True
        elif value == EncoderConstants.FALSE.str_value or value is False:
            return False
        else:
            raise ValueError("Non-boolean input value", value)

    @classmethod
    def unparse_py(cls, value: bool) -> str:
        if value is True:
            return EncoderConstants.TRUE.str_value
        elif value is False:
            return EncoderConstants.FALSE.str_value
        else:
            raise ValueError("Non-boolean output value", value)

    @classmethod
    def unparse_bytes(cls, value: bool) -> bytes:
        if value is True:
            return EncoderConstants.TRUE.value
        elif value is False:
            return EncoderConstants.FALSE.value
        else:
            raise ValueError("Non-boolean output value", value)


class TransportBoolType(TransportBool, TransportType[bool, bool]):
    pass


class TransportFloatStr(TransportInterface[np.double, str]):
    @classmethod
    def parse(cls, value: Union[str, Real]) -> np.double:
        if isinstance(value, np.double):
            return value
        else:
            return np.double(value)

    @classmethod
    def unparse_py(cls, value: np.double, encoder: Optional[JSONEncoder] = None) -> str:
        if __debug__:
            if value == np.nan:
                raise AssertionError("Not serializable for transport", value)
        return str(value)

    @classmethod
    def unparse_bytes(cls, value: np.double) -> bytes:
        return b'"' + super().unparse_bytes(value) + b'"'


class TransportFloatStrType(TransportFloatStr, TransportType[np.double, str]):
    pass


class TransportInt(TransportInterface[int, int]):
    storage_class: ClassVar[type[int]] = int
    @classmethod
    def unparse_py(cls, value: int,
                   encoder: Optional[JSONEncoder] = None) -> int:
        return value

    @classmethod
    def parse(cls, value: int) -> int:
        return value

    @classmethod
    def unparse_url_str(cls, value: int) -> bytes:
        return str(value)

    @classmethod
    def unparse_bytes(cls, value: int) -> bytes:
        return str(value).encode()

    @classmethod
    def unparse_url_bytes(cls, value: int) -> bytes:
        return cls.unparse_bytes(value)


class TransportIntType(TransportInt, TransportType[int, int]):
    pass


class TransportStr(TransportInterface[str, str]):
    storage_class: ClassVar[type[str]] = str

    @classmethod
    def unparse_py(cls, value: str,
                   encoder: Optional[JSONEncoder] = None) -> str:
        return value

    @classmethod
    def parse(cls, value: str) -> str:
        return value

    @classmethod
    def get_display_string(cls, value: str) -> str:
        return value

    @classmethod
    def unparse_bytes(cls, value: str) -> bytes:
        if isinstance(value, str):
            ## ensuring encode for value == ""
            ## given that "" is processed as a false-like value in Python
            return b'"' + value.encode() + b'"'
        elif value is None:
            ## In data from a v20 demo server, str typed fields
            ## may sometimes be provided with a JSON null value
            return EncoderConstants.NULL
        else:
            raise ValueError("Not a string", value)

    @classmethod
    def unparse_url_bytes(cls, value: str) -> bytes:
        return quote_from_bytes(value.encode()).encode()

    @classmethod
    def unparse_url_str(cls, value: str) -> bytes:
        return quote_from_bytes(value.encode())


class TransportStrType(TransportStr, TransportType[str, str]):
    pass


class TransportSecretStr(TransportStr, TransportInterface[SecretStr, str]):

    @classmethod
    def unparse_py(cls, value: SecretStr,
                   encoder: Optional[JSONEncoder] = None) -> str:
        return value.get_secret_value()

    @classmethod
    def parse(cls, value: str) -> SecretStr:
        if isinstance(value, SecretStr):
            return value
        else:
            assert isinstance(value, str), "Received a non-string initializer for SecretStr"
            return cls.storage_class(value)

    @classmethod
    def get_display_string(cls, value: SecretStr) -> str:
        return '**********'

    @classmethod
    def unparse_bytes(cls, value: SecretStr) -> bytes:
        return super().unparse_bytes(value.get_secret_value())

    @classmethod
    def unparse_url_bytes(cls, value: SecretStr) -> bytes:
        return super().unparse_url_bytes(value.get_secret_value())

    @classmethod
    def unparse_url_str(cls, value: SecretStr) -> bytes:
        return super().unparse_url_str(value.get_secret_value())

class TransportSecretStrType(TransportSecretStr, TransportType[SecretStr, str]):
    pass


class TransportIntStr(TransportStr, TransportInterface[int, str]):
    storage_class: ClassVar[type[int]] = int

    ## the server may encode some integer identifiers as string values
    ## e.g TradeID
    @classmethod
    def unparse_py(cls, value: int,
                   encoder: Optional[JSONEncoder] = None) -> str:
        return cls.serialization_class(value)

    @classmethod
    def parse(cls, value: str) -> int:
        return cls.storage_class(value)

    @classmethod
    def unparse_bytes(cls, value: str) -> bytes:
        return super().unparse_bytes(cls.unparse_py(value))

    @classmethod
    def unparse_url_str(cls, value: str) -> str:
        return cls.unparse_py(value)

    @classmethod
    def unparse_url_bytes(cls, value: str) -> bytes:
        cls.unparse_url_str().encode()

    @classmethod
    def get_display_string(cls, value: str) -> str:
        return str(value)


class TransportIntStrType(TransportIntStr[int, str], TransportType[int, str]):
    pass


NullableTimesamp: TypeAlias = Union[datetime, pd.NaT.__class__]


class TransportTimestamp(TransportInterface[datetime, str]):
    """Nullable datetime transport type

    Storage Interface Class: datetime.datetime
    Storage Type: Union[pd.Timestamp, Literal[pd.NaT]]; Compatible with datetime.datetime
    Transport Value Class: str

    The transport string '0' is interpreted symmetrically as pandas.NaT
    """

    ## case study: GetAccountSummary200Response => AccountSummary => resettable_pl_time
    ## - transmitted sometimes as "0".
    ## - when present in the response, the resettable_pl_time "0" must be parsed as some value
    ## - when parsed as a timestamp string, the usage of "0" may lead to unexpected data
    ##   in deserialization, as when value was parsed as a timestamp string
    ##   (e.g using epoch coding) then unparsed from the erroneous timetamp
    ##   (ca. 1970)

    storage_class: ClassVar[type[datetime]] = pd.Timestamp

    @classmethod
    def parse(cls, dt: Union[str, NullableTimesamp]) -> NullableTimesamp:
        if isinstance(dt, pd.Timestamp):
            return dt
        elif isinstance(dt, datetime):
            return pd.to_datetime(dt)
        elif dt is pd.NaT:
            return dt
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
                        logger.critical("Unrecognized timestamp value %r", dt)
                        return pd.NaT

    @classmethod
    def unparse_py(cls, value: NullableTimesamp,
                   encoder: Optional[JSONEncoder] = None) -> str:
        ## Implementation Note:
        ##
        ## pd.NaT may have a particular __eq__ semantics, such that pd.NaT != pd.NaT
        ## while 'a = pd.NaT; a is pd.NaT' would provide a consistent identity relation
        ## in Python
        if value is pd.NaT:
            return "0"
        else:
            return value.isoformat()

    @classmethod
    def unparse_bytes(cls, value: NullableTimesamp) -> bytes:
        if value is pd.NaT:
            ## Implementation Note:
            ##
            ## Although NaT may be parsed from a timestamp '0' in a server response,
            ## NaT values should  generally not be used for requests, whether via form
            ## data or in request URLs.
            ##
            ## Outside of the request scope, the NaT value may be used in JSON
            ## serialization for data from a server response. Consequently,
            ## this transport type supports unparse for NaT, except in URL scope
            return b'0'
        else:
            return TransportStrType.unparse_bytes(value.isoformat(timespec="milliseconds"))

    @classmethod
    def unparse_url_bytes(cls, value: datetime) -> bytes:
        if value is pd.NaT:
            raise ValueError("No URL encoding available for NaT", value)
        else:
            return TransportStrType.unparse_url_bytes(value.isoformat(timespec="milliseconds"))

    @classmethod
    def unparse_url_str(cls, value: datetime) -> bytes:
        if value is pd.NaT:
            raise ValueError("No URL encoding available for NaT", value)
        else:
            return TransportStrType.unparse_url_str(value.isoformat(timespec="milliseconds"))


class TransportTimestampType(TransportTimestamp, TransportType[datetime, str]):
    pass


Tenum = TypeVar("Tenum", bound=MappedEnum)


class TransportEnum(TransportInterface[Tenum, To]):
    storage_class: ClassVar[type[Tenum]] = Enum

    @classmethod
    def check_type(cls, value) -> bool:
        return isinstance(value, cls.storage_class)

    @classmethod
    def parse(cls, serialized: To) -> Union[Tenum, To]:  # type: ignore
        storage_cls: type[Enum] = cls.storage_class
        map = storage_cls._member_map_
        if serialized in map:
            return map[serialized]  # type: ignore
        elif serialized in storage_cls._value2member_map_:
            return storage_cls._value2member_map_[serialized]
        else:
            return storage_cls[serialized]

    @classmethod
    def unparse_py(cls, venum: Tenum,
                   encoder: Optional[JSONEncoder] = None) -> To:
        return venum.value

    @classmethod
    def unparse_bytes(cls, value: Tenum) -> bytes:
        return b'"' + bytes(value) + b'"'

    @classmethod
    def unparse_url_bytes(cls, value: Tenum) -> bytes:
        return bytes(value)

    @classmethod
    def unparse_url_str(cls, value: Tenum) -> bytes:
        return str(value)


class TransportEnumType(TransportEnum, TransportType[Tenum, To]):
    pass


class TransportEnumStrType(TransportEnumType[Tenum, str]):
    pass


class TransportEnumIntType(TransportEnumType[Tenum, int]):
    pass


__all__ = exporting(__name__, ..., typevars=True)
