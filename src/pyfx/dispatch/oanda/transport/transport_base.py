## base types for transport type, transport field definitions

from collections.abc import Collection, Sequence, Sequence
from json import JSONEncoder
from types import NoneType
from typing import Generic, Optional, TypeAlias, Union
from typing_extensions import ClassVar, Generic, TypeAlias, TypeVar, Union, get_args, get_origin, get_original_bases

from pydantic import BaseModel
from pydantic.fields import FieldInfo

from ..util.typeref import get_type_class
from ..util.naming import exporting

## memoization for ApiClient.sanitize_for_serialization
JsonLiteral: TypeAlias = Union[float, bool, bytes, str, int]

Ti = TypeVar("Ti")
To = TypeVar("To")

InitArg = TypeVar("InitArg")


def get_sequence_member_class(spec: TypeAlias) -> type:
    # if __debug__:
    #     if not isinstance(spec, GenericAlias):
    #         raise AssertionError("Not a generic alias type specifier", spec)
    origin = get_origin(spec)
    if origin == Union:
        ## parse a stored type alias from an Optional[concrete_type] declaration
        args = get_args(spec)
        if args and len(args) is int(2) and args[-1] == NoneType:
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


class TransportTypeBase(type, Generic[Ti, To]):
    ## initialization shim for TransportType processing in TransportTypeClass.__new__
    ##
    ## in effect, defines a named union type
    pass


class TransportTypeClass(type):

    def initialize_attrs(cls):
        attrs = cls.__dict__
        ## set the transport storage and serialization classes for the new TransportTypeClass,
        ## based on args provided to the TransportTypeBase generic type
        for gen_base in get_original_bases(cls):
            origin = get_origin(gen_base)
            if origin and issubclass(origin, TransportTypeBase):
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


class TransportType(TransportTypeBase[Ti, To], Generic[Ti, To], metaclass=TransportTypeClass):

    storage_type: ClassVar[Union[type, TypeAlias]]
    """Effective storage type for values of this transport type"""

    storage_class: ClassVar[type]
    """Storage interface class for values of this transport type


    The default `parse()` method will apply this class name as
    a constructor function. The function will be provided with the
    intermediate transport value received by `parse()
    """

    serialization_type: ClassVar[Union[type, TypeAlias]]
    """Intermediate serialization type for protocol data encoding

    For a transport type serialized to JSON, this type would typically
    denote the type of value processed by the JSON encoder or decoder.
    """

    serialization_class: ClassVar[type]
    """Intermediate serialization class for protocol data encoding

    For a transport type serialized to JSON, this class would typically
    denote the class of value processed by the JSON encoder or decoder.

    The default `unparse()` method will apply this class name as a constructor
    function to the value provided to `unparse()`. The object returned by the
    constructor will be passed to the transport encoder provided to `unparse()`
    """

    @classmethod
    def unparse(cls, value: Ti, encoder: JSONEncoder) -> To:
        """Return a serializable object representation for a value
        of this transport type.

        The return value should be produced in a type compatible with
        this transport type's serialization encoding. Structurally, the
        value should have a syntax generally similar to the syntax for
        the return value of json.JSONEncoder.default()

        Params:
        value: the value to unparse
        decoder: a JSONEncoder instance.

        Returns: the encoded object, in this transport type's
        serialization encoding
        """

        ## decoder: JSON decoder for structured object deserializtion.
        ##
        ## If provided, the decoder should be applied for deserializing
        ## structured elements of the value. To apply the decoder about
        ## the value itself would likely result in a loop
        ##
        ## Assumption: The decoder will not need to check for circular
        ## object references.
        ##
        ## This default method is applicable for literal serialization
        ## types only
        return encoder.default(cls.serialization_class(value))

    @classmethod
    def parse(cls, unparsed: To) -> Ti:
        if __debug__:
            ## generalized TransportType has no storage class defined
            if not hasattr(cls, "storage_class"):
                raise AssertionError("No storage_class defined", cls)
        return cls.storage_class(unparsed)

    @classmethod
    def __init_subclass__(cls, *args, **kw):
        # utility function for application after new_class() and within cls.__new__()
        super().__init_subclass__
        cls.initialize_attrs()


class TransportFieldInfo(FieldInfo, Generic[Ti, To]):
    '''FieldInfo base class for transport fields'''

    transport_type: TransportType[Ti, To]
    storage_class: type
    field_name: str
    defining_class: type[BaseModel]
    deprecated: bool

    __slots__  = tuple(frozenset(list(FieldInfo.__slots__) + ["transport_type", "defining_class", "field_name", "storage_class", "deprecated"]))

    def __init__(self, default, transport_type: TransportType[Ti, To], deprecated=None, **kw):
        # implementation note: the field's transport type will be
        # further processed duirng ApiObject class initialization,
        # mainly to replace any TransportTypeInfer type with a
        # transport type determined from metadata for the field,
        # at the class scope
        self.transport_type = transport_type
        self.deprecated = deprecated
        super().__init__(default=default, **kw)

    @classmethod
    def from_field(cls, default, transport_type: TransportType[Ti, To], **kw):  # type: ignore
        return cls(default, transport_type=transport_type, **kw)

    def __repr__(self):
        defining = self.defining_class.__qualname__ if hasattr(self, "defining_class") else "<Undefined>"
        field = self.field_name if hasattr(self, "field_name") else "<Undefined>"
        return "<%s [%s.%s]>" % (self.__class__.__qualname__, defining, field)


class TransportTypeInfer(TransportType[None, None]):
    """Intemerdiate TransportType

    The presence of the class TransportTypeInfer as the transport type for a
    TransportFieldInfo definition will indicate that the transport type for
    the corresponding class field should be inferred from field annotations.
    """
    pass


TRANSPORT_VALUES_STORAGE_CLASS: TypeAlias = list
"""Storage class for internal representation of JSON array values"""


class TransportValues(TransportType[TRANSPORT_VALUES_STORAGE_CLASS[Ti], list[To]], Generic[Ti, To]):
    member_transport_type: TransportType[Ti, To]

    @classmethod
    def get_storage_class(cls):
        return list

    @classmethod
    def parse_member(cls, value: To) -> Ti:
        return cls.member_transport_type.parse(value)

    @classmethod
    def unparse_member(cls, value: Ti, encoder: JSONEncoder) -> To:
        return cls.member_transport_type.unparse(value, encoder)

    @classmethod
    def parse(cls, unparsed: list[To]) -> TRANSPORT_VALUES_STORAGE_CLASS[Ti]:
        return [cls.parse_member(elt) for elt in unparsed]

    @classmethod
    def unparse(cls, value: list[Ti],
                encoder: JSONEncoder) -> list[To]:
        return [cls.unparse_member(elt, encoder) for elt in value]

    @classmethod
    def __init_subclass__(cls, *, member_class=None, **kw):
        if member_class:
            ## if not provided, member_class should be initialized later
            cls.member_transport_type = member_class
        super().__init_subclass__(**kw)


__all__ = exporting(__name__, ..., typevars=True)
