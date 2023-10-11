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

Ti = TypeVar("Ti", bound=JsonLiteral)
To = TypeVar("To", bound=JsonLiteral)

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


class TransportTypeBase(Generic[Ti, To], type):
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

    storage_type: ClassVar[Union[type, TypeAlias]]  # input type for the field definition, may or may not represent a single class
    storage_class: ClassVar[type]  # generally represented in the field annotation, but here as a single input value class

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
        ## generic TransportType has no storage class defined ...
        ## seen for a bug in transport type initialization for enum values
        ## given the buggy enum value type definitions in .models, etc
        if __debug__:
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

    @property
    def transport_type(self) -> TransportType[Ti, To]:
        return self._transport_type

    @transport_type.setter
    def transport_type(self, t: TransportType[Ti, To]):
        self._transport_type = t

    @property
    def storage_class(self) -> type:
        return self._storage_class

    @transport_type.setter
    def storage_class(self, t: type):
        self._storage_class = t

    @property
    def defining_class(self) -> type[BaseModel]:
        return self._defining_class

    @defining_class.setter
    def defining_class(self, value: type[BaseModel]):
        ## this property should be immutable after initialization of the defining class
        if hasattr(self, "_defining_class") and self._defining_class is not value:
            raise ValueError("defining_class already defined", self._defining_class, self, value)
        else:
            self._defining_class = value

    @property
    def field_name(self) -> str:
        return self._field_name

    @field_name.setter
    def field_name(self, name: str):
        if hasattr(self, "_field_name"):
            raise ValueError("field_name already defined", self.field_name, self, name)
        else:
            self._field_name = name

    @property
    def deprecated(self) -> Optional[bool]:
        return self._deprecated

    __slots__: ClassVar[frozenset[str]] = frozenset(list(FieldInfo.__slots__) + ["_transport_type", "_defining_class", "_field_name", "_storage_class", "_deprecated"])

    def __init__(self, default, transport_type: TransportType[Ti, To], deprecated=None, **kw):
        # implementation note: the field's transport type will be
        # further processed duirng ApiObject class initialization,
        # mainly to replace any TransportTypeInfer type with a
        # transport type determined from metadata for the field,
        # at the class scope
        self.transport_type = transport_type
        self._deprecated = deprecated
        super().__init__(default=default, **kw)

    @classmethod
    def from_field(cls, default, transport_type: TransportType[Ti, To], **kw):
        return cls(default, transport_type=transport_type, **kw)

    def __repr__(self):
        defining = self.defining_class.__qualname__ if hasattr(self, "_defining_class") else "<Undefined>"
        field = self.field_name if hasattr(self, "_field_name") else "<Undefined>"
        return "<%s [%s.%s]>" % (self.__class__.__qualname__, defining, field)


class TransportTypeInfer(TransportType[object, object]):
    """Intemerdiate TransportType

    The presence of the class TransportTypeInfer as the transport type for a 
    TransportFieldInfo definition will indicate that the transport type for 
    the corresponding class field should be inferred from field annotations.
    """
    pass


TRANSPORT_VALUES_STORAGE_CLASS: type[Collection] = list
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
