## base types for transport data model

from abc import ABC
from collections.abc import Mapping
from datetime import datetime
from enum import Enum
# from reprlib import repr
from immutables import Map
from json import JSONEncoder
import logging
from numpy import datetime64, double
from pandas import Timestamp
from pydantic import ConfigDict, BaseModel
from pydantic.fields import PydanticUndefined
from pydantic._internal._model_construction import ModelMetaclass
from reprlib import repr
import sys
from types import new_class, NoneType
from typing import Any, Generic, Iterable, Iterator, Optional, TypeAlias, Union, TYPE_CHECKING
from typing_extensions import ClassVar, Self, TypeVar, TypeAlias, Union, get_origin, get_type_hints

from ..finalizable import FinalizableClass
from ..util.typeref import get_type_class, get_literal_value, resolve_forward_reference
from ..util.naming import exporting
from .transport_common import IntermediateObject

from .transport_base import (
    # fmt: off
    TransportInterface,
    TransportFieldInfo, TransportType, TransportTypeClass, TransportTypeInfer,
    TransportValuesType, TransportBoolType, TransportNoneType, TransportIntType, TransportStrType,
    TransportFloatStrType, TransportTimestampType
    # fmt: on
)
from .application_fields import ApplicationFieldInfo
from .repository import TransportBaseRepository
from .encoder_constants import EncoderConstants

logger = logging.getLogger(__name__)

FieldName: TypeAlias = str

T_typ = TypeVar("T_typ", bound=type)


class TransportModelRepository(TransportBaseRepository):

    @classmethod
    def initialize_singleton(cls):
        singleton = super().initialize_singleton()
        singleton.bind_types({
            bool: TransportBoolType,
            NoneType: TransportNoneType,
            str: TransportStrType,
            int: TransportIntType,
            float: TransportFloatStrType,
            double: TransportFloatStrType,
            datetime: TransportTimestampType,
            datetime64: TransportTimestampType,
            Timestamp: TransportTimestampType,
        })
        return singleton

    def make_object_transport_type(self, value_type: "type[ApiObject]") -> type[TransportType]:
        assert issubclass(value_type, ApiObject), "Not an ApiObject type"
        name = "Transport_" + value_type.__name__

        def init_ns(ns: dict[str, Any]):
            nonlocal value_type
            ns["storage_type"] = value_type
            ns["storage_class"] = value_type

        typ: TransportTypeClass[TransportObjectType] = new_class(name, (TransportObjectType,), None, init_ns)  # type: ignore[assignment]

        typ.initialize_attrs()

        self.direct_types_map[value_type] = typ  # type: ignore[index]
        return typ

    def get_transport_type(self, value_type: type | TypeAlias,
                           storage_class: Optional[type] = None) -> TransportType:
        storage_cls = storage_class or get_type_class(value_type)
        found = self.find_transport_type(value_type, storage_cls)
        if found:
            return found
        elif self.__finalized__:
            raise ValueError("Repository is finalized", self)
        elif issubclass(storage_cls, ApiObject):
            # Create a new transport type for the ApiObject class
            new_type = self.make_object_transport_type(storage_cls)
            # register and return the new transport type
            self.bind_transport_type(storage_cls, new_type)
            return new_type
        else:
            return super().get_transport_type(value_type)


JsonTypesRepository: TransportModelRepository = TransportModelRepository.__singleton__


class InterfaceClass(ModelMetaclass, FinalizableClass, ABC):

    json_fields: Mapping[str, TransportFieldInfo]
    """Mapping of JSON field names to field info objects"""

    json_field_names: Mapping[str, str]
    ## used for model object unparse
    """Mapping of each instance field name to its JSON field name"""

    transport_type: "TransportObjectType"
    """When bound, the transport type for the class onto the class' types repository"""

    api_storage_fields: frozenset[str]
    """This field is Documented as a class variable in ApiObject"""

    types_repository: "TransportModelRepository"
    """This field is Documented as a class variable in ApiObject"""

    @classmethod
    def default_model_config(cls):
        return ConfigDict(
            populate_by_name=True,
            arbitrary_types_allowed=True,
            validate_assignment=__debug__,
            # alias_priority=2,  # type: ignore[typeddict-unknown-key]
            strict=False,
        )

    @classmethod
    def get_instance_annotations(cls) -> Mapping[str, Any]:
        annotations = dict()
        for mcls_base in cls.__mro__:
            for attr, annot in get_type_hints(mcls_base).items():
                if not (get_origin(annot) is ClassVar or attr in annotations):
                    annotations[attr] = ClassVar[annot]
        return annotations

    #
    # instance methods for InterfaceClass initialization
    #
    # Except for __finalize__, these methods are called mainly during __new__
    #

    def __finalize_instance__(cls):
        if not cls.__finalized__:
            cls.ensure_transport_type()
            if hasattr(cls, "model_fields"):
                cls.model_fields = Map(cls.model_fields)
            else:
                cls.model_fields = Map({})
            if hasattr(cls, "json_fields"):
                cls.json_fields = Map(cls.json_fields)
            else:
                cls.json_fields = Map({})
            super().__finalize_instance__()

    def default_types_repository(self) -> TransportBaseRepository:
        """Return the default transport types repository for this class.

        This repository will be used for protocol class definitions, generally
        when a `types_repository` was not provided during class initialization.
        """
        return JsonTypesRepository

    def ensure_transport_type(self) -> Optional[TransportType]:
        """If the class `self` is not defined with `ABC` as a direct base class,
        ensure that a transport type binding is defined for the class,
        in the class' types repository.

        Derived classes may override this method.
        """
        if ABC in self.__bases__:
            return None
        if not hasattr(self, "transport_type"):
            self.transport_type = self.types_repository.get_transport_type(self)  # type: ignore[assignment]
        return self.transport_type

    def init_field_info(self, field_name: str, info: TransportFieldInfo):
        """Initialize TransportFieldInfo attributes for the `info` metaobject in the class `self`"""

        info.bind(field_name, self)

        if not isinstance(info, TransportFieldInfo):
            return

        ttype = info.transport_type
        if __debug__:
            if ttype and not isinstance(ttype, type):
                # fmt: off
                raise AssertionError("Not a type", ttype, info, self)
                # fmt: on
        if (ttype is TransportTypeInfer) or (not ttype):
            field_hint = get_type_hints(self).get(field_name)
            if __debug__:
                if not field_hint:
                    # generally not reached - pydantic would typically catch the instance
                    # of a field defined without type hints/annotations
                    raise AssertionError("No type hints provided for field", field_name, self, get_type_hints(self))
            if not hasattr(info, "value_type"):
                info.value_type = field_hint
            field_type = get_type_class(field_hint)  # may fail, for some not-really-complex param type hitns
            if issubclass(field_type, TransportType):
                # the field's concrete type is a transport type
                #
                # generally for types defined in ..common_types
                info.transport_type = field_type
                info.storage_class = field_type.storage_class
            elif field_hint:
                typ = self.types_repository.get_transport_type(field_hint)
                if not typ:
                    # fmt: off
                    raise ValueError("Repository returned no transport type", field_hint, field_name, self)
                    # fmt: on
                info.transport_type = typ
                info.storage_class = get_type_class(field_hint)
            else:
                # assumption: the new_cls may represent a generalized type
                pass

    def get_transport_type(self, value_type: Union[type, TypeAlias]) -> TransportType:
        """Forward a transport type query to the types repository of the class `self`

        Raises AttributeError if the class does not provide a `types_repository` attribtue value"""
        return self.types_repository.get_transport_type(value_type)

    def __new__(mcls, cls_name: str, bases: tuple[type, ...], namespace: dict[str, Any], **kw):
        if "model_config" not in namespace:
            namespace["model_config"] = mcls.default_model_config()

        ## inherit non-ClassVar annotations as class instance annotations for each class in cls.__mro__
        annotations = namespace["__annotations__"] if "__annotations__" in namespace else {}
        annotations.update(mcls.get_instance_annotations())
        namespace["__annotations__"] = annotations

        to_finalize = namespace.get("__finalized__", False)
        if to_finalize:
            # removing __finalized__ attr temporarily, before finalize()
            del namespace["__finalized__"]

        ## inherit InterfaceClass instance annotations as instance ClassVar annotations
        annotations = namespace["__annotations__"] if "__annotations__" in namespace else {}
        for attr, annot in get_type_hints(InterfaceClass).items():
            if not (get_origin(annot) is ClassVar or attr in annotations):
                annotations[attr] = ClassVar[annot]
        namespace["__annotations__"] = annotations

        ## note that mcls.__pydantic_init_subclass__ would be called under the following:
        new_cls: "InterfaceClass" = super().__new__(mcls, cls_name, bases, namespace, **kw)

        #
        # post-initialization
        #

        repository = new_cls.types_repository if hasattr(new_cls, "types_repository") else None
        if not repository:
            ## ensuring a types repository is available, before finalizing any transport
            ## field definitions for the class
            for bcls in bases:
                ## first try to inherit any types repository from the class of a base class
                mcls = bcls.__class__
                if InterfaceClass in mcls.__mro__ and hasattr(mcls, "types_repository"):
                    new_cls.types_repository = mcls.types_repository
                    break
            if not hasattr(new_cls, "types_repository"):
                ## else use default
                new_cls.types_repository = new_cls.default_types_repository()

        model_fields = new_cls.model_fields

        for name, info in model_fields.items():
            new_cls.init_field_info(name, info)

        json_field_names = Map({name: info.alias or name for name, info in model_fields.items()})
        json_fields = Map({json_name: model_fields[name] for name, json_name in json_field_names.items()})
        new_cls.json_fields = json_fields
        new_cls.json_field_names = json_field_names

        ## common
        new_cls.api_storage_fields = frozenset({"__pydantic_fields_set__", "__pydantic_extra__", "__pydantic_private__"})

        new_cls.ensure_transport_type()


        return new_cls


    #     Known Limitation:

    #     The implementation should ensure that all required transport
    #     types have been defined to the corresponding types repository,
    #     before calling this method. Subsequent of finaliztion, the
    #     repository will generally not accept new transport type
    #     definitions.
    #     """
    #     if not cls.__finalized__:
    #         cls.types_repository.finalize()
    #         super().finalize()


class ApiClass(InterfaceClass, ABC):

    api_transport_fields: frozenset[str]  # ApiClass conly
    """This field is Documented as a class variable in ApiObject"""

    # @staticmethod
    def __new__(mcls, cls_name: str, bases: tuple[type, ...], namespace: dict[str, Any]):

        if "api_transport_fields" not in namespace:
            transport_fields = set(namespace.get("api_transport_fields", ()))
            for base in bases:
                if ApiClass in base.__class__.__mro__:
                    transport_fields = transport_fields.union(base.api_transport_fields)
            transport_fields = frozenset(transport_fields)
            namespace["api_transport_fields"] = transport_fields

        new_cls = super().__new__(mcls, cls_name, bases, namespace)

        def filter_default(item: tuple[str, TransportFieldInfo]) -> bool:
            ## when default == PydanticUndefined: e.g for a default provided to the field info as '...'
            return item[1].default is not None
        ## for all fields with a defined, non-None default, ensure the field's Python name will be added
        ## to api_transport_fields
        transport_post = frozenset(new_cls.api_transport_fields) | frozenset(map(lambda item: item[0], filter(filter_default, new_cls.model_fields.items())))
        new_cls.api_transport_fields = transport_post

        return new_cls


Ts = TypeVar("Ts", bound="ApiObject")


class ModelState(Generic[Ts]):
    __slots__ = ("state", "model_class")
    state: Map[str, Any]
    model_class: "type[Ts]"

    @property
    def model_fields(self) -> Mapping[str, TransportFieldInfo]:
        return self.model_class.model_fields  # type: ignore[return-value]

    @classmethod
    def get_field_state(cls, obj: "ApiObject", name: str):
        model_fields = obj.__class__.model_fields
        if name in model_fields:
            transport_type: TransportType = model_fields[name]
            return transport_type.get_state(getattr(obj, name))
        else:
            return getattr(obj, name)

    @classmethod
    def derive_state(cls, m_object: Ts) -> "ModelState[Ts]":
        m_cls = m_object.__class__
        fields = tuple(m_object.api_storage_fields.union(m_object.__pydantic_fields_set__))
        dmap = {f: cls.get_field_state(m_object, f) for f in m_object.api_storage_fields.union(m_object.__pydantic_fields_set__)}
        return ModelState(Map(dmap), m_object.__class__)

    def __init__(self, state: Map[str, Any], cls: type[Ts]):
        self.state = state
        self.model_class = cls

    def __getattr__(self, attr: str) -> Any:
        if attr in self.model_fields:
            return self.state[attr]
        else:
            raise AttributeError("Unknown model field", attr)

    def __getitem__(self, name: str) -> Any:
        return self.state.__getitem__(name)

    def keys(self) -> Iterable[str]:
        return self.state.keys()

    def values(self) -> Iterable:
        return self.state.values()

    def items(self) -> Iterable[tuple[str, Any]]:
        return self.state.items()

    def __iter__(self) -> Iterator[str]:
        return self.state.__iter__()


Tobject = TypeVar("Tobject", bound="ApiObject")


class TransportObject(TransportInterface[Tobject, IntermediateObject]):

    storage_class: Tobject

    @classmethod
    def parse(cls, unparsed: Union[Tobject, IntermediateObject]) -> Tobject:
        if isinstance(unparsed, cls.storage_class):
            # handle partial deserialization under the initial parse from stream
            return unparsed  # type: ignore
        else:
            assert isinstance(unparsed, Mapping), "Not a mapping value"
            model_cls: Union[type["ApiObject"], type["AbstractApiObject"]] = cls.storage_class
            if issubclass(model_cls, AbstractApiObject) and ABC in model_cls.__bases__:
                key = model_cls.designator_key
                designator = unparsed[key]
                model_cls = model_cls.class_for_designator(designator)
            json_fields = model_cls.json_fields
            info = None
            inst = model_cls.__new__(model_cls)
            for key, unparsed_value in unparsed.items():
                if key in json_fields:
                    info = json_fields[key]
                else:
                    raise ValueError("Unknown JSON field", key, model_cls)
                ttyp = info.transport_type
                parsed = ttyp.parse(unparsed_value)
                attr = info.name
                setattr(inst, attr, parsed)
                # object.__setattr__(inst, attr, parsed)
            return inst

    @classmethod
    def unparse_py(cls, o: Tobject, encoder: JSONEncoder) -> IntermediateObject:
        m = dict()
        mcls = o.__class__
        fields = mcls.model_fields
        json_names = mcls.json_field_names
        for name in o.__pydantic_fields_set__.union(mcls.api_transport_fields):
            field_info: TransportFieldInfo = fields[name]  # type: ignore[assignment]
            if __debug__:
                if not isinstance(field_info, TransportFieldInfo):
                    raise AssertionError("Not a TransportFieldInfo", field_info)
            name: str = json_names[name]
            transport_type: TransportType = field_info.transport_type
            val = getattr(o, name)
            if val is None:
                m[name] = "null"
            else:
                val = transport_type.unparse_py(val, encoder)
                m[name] = val
        return m

    @classmethod
    def iter_transport_field_bytes(cls, obj: Tobject):
        dq = EncoderConstants.DQUOTE
        dq_key_sep = EncoderConstants.DQUOTE_KEY_SEPARATOR
        model_fields = obj.__class__.model_fields
        for name in cls.storage_class.api_transport_fields.union(obj.model_fields_set):
            field: TransportFieldInfo = model_fields.get(name, None)

            attrval = getattr(obj, name) if hasattr(obj, name) else field.default
            if attrval is PydanticUndefined:
                raise ValueError("no value set for required field", name, obj)
            json_name = field.json_name_bytes
            if field:
                unparsed_value = field.transport_type.unparse_bytes(attrval)
                yield dq + json_name + dq_key_sep + unparsed_value
            else:
                raise KeyError("Field has no model definition", name, obj.__class__)

    @classmethod
    def unparse_bytes(cls, value: Tobject) -> bytes:
        sep = EncoderConstants.ITEM_SEPARATOR
        return EncoderConstants.START_MAP.value + sep.join(
            expr for expr in cls.iter_transport_field_bytes(value)
        ) + EncoderConstants.END_MAP.value

    @classmethod
    def unparse_url_bytes(cls, value: Tobject) -> bytes:
        ## v20 API is based on OpenAPI 2 / Swagger.
        ## JSON encoding for URL query strings is introduced in OpenAPI 3
        raise ValueError("ApiModel objects cannot be URL encoded")

    @classmethod
    def unparse_url_str(cls, value: Tobject) -> bytes:
        ## v20 API is based on OpenAPI 2 / Swagger.
        ## JSON encoding for URL query strings is introduced in OpenAPI 3
        raise ValueError("ApiModel objects cannot be URL encoded")


class TransportObjectType(TransportObject, TransportType[Tobject, IntermediateObject]):
    pass


class InterfaceModel(BaseModel, ABC, metaclass=InterfaceClass):

    if TYPE_CHECKING:
        model_fields: ClassVar[Mapping[str, ApplicationFieldInfo]]

    __finalize__: ClassVar[bool] = False
    """Finalization state flag for the ApiObject class"""

    validate_fields: ClassVar[bool] = __debug__
    """Configuration property for Pydantic 2"""

    types_repository: ClassVar[TransportBaseRepository]
    """Types repository for transport and storage encoding onto this class"""

    transport_type: ClassVar["TransportObjectType"]
    """Transport type for this ApiObject class, if bound

    This attribute may be unbound in the class scope, such as generally
    when the class does not represent a concrete model implementation type,
    mainly with the ApiObject and AbstractApiObject classes.

    This attribute's value would generally be initialized within the
    class method `ensure_transport_type()`
    """

    #
    # InterfaceModel initialization
    #

    # @staticmethod
    def __new__(cls, **kw):
        """construct an InterfaceModel without field validation

        `kw`: Optional mapping of field names and field values for the new instance

        Known Limitations:
        - The new instance will not have been validated for whether all required model
          fields have been set
        - Field values provided in `kw` will not have been validated for syntax
        - Default field values will not have been set in the new instance. Each default
          value should nonethless be accessible via `getattr()` for the instance
        """
        inst = super().__new__(cls)
        object.__setattr__(inst, "__pydantic_extra__", None)
        for arg, value in kw.items():
            object.__setattr__(inst, arg, value)
        fields_kw = set(cls.model_fields.keys()).intersection(set(kw.keys()))
        object.__setattr__(inst, "__pydantic_fields_set__", fields_kw)
        return inst

    @classmethod
    def new(cls, **kw):
        """construct an InterfaceModel with field validation"""
        return cls.model_construct(**kw)

    def __init__(self, *args, **kwargs):
        fields = self.__class__.model_fields
        kw = dict(kwargs) if kwargs else kwargs
        for name, value in kwargs.items():
            if name in fields:
                info: TransportFieldInfo = fields[name]
                if isinstance(info, TransportFieldInfo):
                    txtyp = info.transport_type
                    if issubclass(txtyp, TransportValuesType):
                        mtyp = txtyp.member_transport_type
                        mcls = mtyp.storage_class
                        kw[name] = [elt if isinstance(elt, mcls) else mtyp.parse(elt) for elt in value]
                    else:
                        scls = txtyp.storage_class
                        if not isinstance(value, scls):
                            kw[name] = txtyp.parse(value)
        super().__init__(*args, **kw)

    #
    # attr wrappers for model fields
    #

    def __getattr__(self, attr: str,  assume_model: bool = False) -> Any:
        """If the `key` name denotes a model field for the instance not present in
        `self.model_fields_set`, returns the default value for that field. Else,
        returns the value from the superclass' `__getattr__()` function

        If the `key` name denotes a required model field and the field is unset in
        this instance, raises AttributeError.
        """
        fields = self.__class__.model_fields
        if assume_model or attr in fields:
            if attr in self.model_fields_set:
                return super().__getattr__(attr)  # type: ignore
            ## return the default value for the named field, if available
            field = fields[attr]
            default = field.default
            if default is PydanticUndefined:
                # fmt: off
                raise AttributeError("Field is unset and has no default value", attr)
                # fmt: on
            else:
                return default
        else:
            return super().__getattr__(attr)  # type: ignore

    def __setattr__(self, attr: str, value: Any, assume_model: bool = False) -> Any:
        fields = self.__class__.model_fields
        if assume_model or attr in fields:
            info = fields[attr]
            if isinstance(info, TransportFieldInfo):
                txtyp = info.transport_type
                scls = txtyp.storage_class
                if not isinstance(value, scls):
                    # Implementation Note:
                    # This will typically not be reached during __init__()
                    return super().__setattr__(attr, txtyp.parse(value))
        return super().__setattr__(attr, value)

    def __delattr__(self, name: str, assume_model: bool = False):
        """unset a model field for the object

        remove the provided attribute name from the set of "set"
        fields for the instance and set the default value defined
        in field information for the attribute.

        For a `name` not matching a model field for the instance,
        raises AttributeError

        If no default value is avaialble, raises AttributeError
        before modifying the instance.

        This function assumes that the `name` is provided in the
        Python syntax for the model field, rather than using a
        model field alias name.

        Known Limitations:
        - Not thread-safe for concurrent read and modification of model fields
        """
        fields = self.__class__.model_fields
        if assume_model or name in fields:
            field = fields[name]
            default = field.default
            if default is PydanticUndefined:
                raise AttributeError("Unable to unset a field with no default value", name)
            self.__setattr__(self, name, default, True)
            self.__pydantic_fields_set__.remove(name)
        else:
            raise AttributeError("Model field not found", name)

    #
    # Items -> attr interface for model fields
    #

    def __getitem__(self, key: str, assume_model: bool = False) -> Any:
        """Set the value for the attribute `key`, if `key` denotes a model field.

        This function provides support for a subscript syntax in accessing model
        attributes of an ApiObject.

        For a `key` not matching a model field for the instance, raises KeyError."""
        fields = self.__class__.model_fields
        if assume_model or key in fields:
            return self.__getattr__(self, key, True)
        else:
            raise KeyError("Model field not found", key)

    def __setitem__(self, key: str, value: Any, assume_model: bool = False) -> Any:
        """Set the value for the attribute `key`, if `key` denotes a model field.

        This function provides support for a subscript syntax in accessing model
        attributes of an ApiObject.

        For a `key` not matching a model field for the instance, raises KeyError.

        Known Limitations:
        - Not thread-safe for concurrent read and modification of model fields
        """
        if __debug__:
            if hasattr(self, "__state__"):
                raise ValueError("Object is immutable", self)
        if assume_model or key in self.__class__.model_fields:
            return setattr(self, key, value)
        else:
            raise KeyError("Model field not found", key)

    def __delitem__(self, key: str, assume_model: bool = False) -> Any:
        """remove the provided `key` from the set of "set" fields for the instance
        and set the default value for the attribute named in `key`.

        This function provides support for a subscript syntax in effectively
        deleting a model attribute from an ApiObject.

        For a `key` not matching a model field for the instance, raises KeyError.

        If no default value is avaialble, raises KeyError before modifying the instance.

        This function assumes that the `key` is provided in the Python syntax for the model
        field, rather than using a model field alias name.

        Known Limitations:
        - Not thread-safe for concurrent read and modification of model fields

        see also: __delattr__()
        """
        fields = self.__class__.model_fields
        if assume_model or key in fields:
            return self.__delattr__(key, True)
        else:
            raise KeyError("Model field not found", key)

    #
    # repr, str
    #

    def __repr__(self, cache: Optional[list] = None):
        # fmt: off
        return self.__class__.__qualname__ + "(" + ", ".join({field + "=" + repr(getattr(self, field)) for field in self.model_fields_set}) + ")"
        # fmt: on

    def __str__(self):
        # fmt: off
        return self.__class__.__qualname__ + "(" + ", ".join({field + "=" + str(getattr(self, field)) for field in self.model_fields_set}) + ")"
        # fmt: on


class ApiObject(InterfaceModel, ABC, metaclass=ApiClass):

    if TYPE_CHECKING:
        model_fields: ClassVar[Mapping[str, TransportFieldInfo]]

    api_transport_fields: ClassVar[frozenset[str]]
    """Fields to serialize for transport

    A set-wise listing of field names, for fields that should always be serialized
    to a transport  stream.

    Values for these fields will be serialized, whether or not the field is denoted
    in `__pydantic_fields_set__` for the instance. Each correspnding field must
    therefore be set in the instance, or must have been defined with a default
    value or default facdtory.
    """

    api_storage_fields: ClassVar[frozenset[str]]
    """Fields to serialize for storage

    Memoized storage for field names, denoting the set of fields that should be
    processed for serialization to storage, complimentary to fields that would
    be serialized for transport for a given instance of this class

    Similar to the value of `api_transport_fields`, this would be supplemental
    to the instance-scoped set of field names `__pydantic_fields_set__` for
    each ApiObject instance.

    Each field denoted in this set must be set in the instance, or the field
    must have been defined with a default value or default factory.
    """

    #
    # serialization state and hashing support
    #

    def __getstate__(self) -> ModelState[Self]:  # type: ignore[override]
        # -> Map[str, Any]:
        """Return an immutable mapping, representative of the object for
        applications in serialization for storage

        The object may be considered immutable after this method has been
        called.
        """
        if hasattr(self, "__state__"):
            return self.__state__
        else:
            cls = self.__class__
            if not hasattr(cls, "transport_type"):
                cls.ensure_transport_type()
            return self.transport_type.get_state(self)

    def __setstate__(self, state: ModelState[Self]):  # type: ignore[override]
        # utility method for object initialization under ZODB
        #
        # Implementation Note: This will dispatch to object.setattr()
        #
        # - This avoids a call to BaseModel.__setattr__() such that may fail
        #   when __pydantic_private__ has not yet been set
        #
        # - It's assumed that the `state`  data would be from a trusted and
        #   API-compatible source
        #
        for attr, value in state.items():
            object.__setattr__(self, attr, value)
        self.__state__ = state

    def __hash__(self) -> int:
        return hash(self.__getstate__())

    def __eq__(self, other: Any) -> bool:
        if id(self) is id(other):
            return True
        elif self.__class__ is not other.__class__:
            return False
        return self.__getstate__() == other.__getstate__()

    #
    # methods after the original .models.* classes produced with OpenAPI Generator
    #

    def to_json_str(self) -> str:
        """Return a JSON string representation of the object"""
        return self.transport_type.unparse_bytes(self).decode()

    def to_json_bytes(self) -> bytes:
        """Return a JSON bytes representation of the object"""
        return self.transport_type.unparse_bytes(self)

    @classmethod
    def from_json(cls, json_data: Union[str, bytes]) -> Self:
        """Create an instance of the ApiObject class from a JSON string"""
        ## localizing the import to the method scope should serve to prevent
        ## a circular dependency from ..parser
        from ..parser import ModelBuilder
        return ModelBuilder.from_text(cls, json_data)

    @classmethod
    def from_dict(cls, obj: Optional[Union[Mapping[str, Any], Self]]) -> Self:
        """Create an instance of the ApiObject class from a mapping value"""
        return cls.model_validate(obj)

    def to_transport_dict(self, encoder: JSONEncoder, by_alias: bool = False):
        """Return an intermediate dictionary representation of the object.

        Each field name in the dictionary will be encoded with the class' internal field
        name if `by_alias` is false, else using any JSON alias name when applicable.

        Each field value will be encoded with an intermediate value representation.
        The syntax for this representation should be compatible with conventions
        for JSON encoding/decoding in Python."""
        enc = encoder or JSONEncoder(check_circular=False, ensure_ascii=False)
        cls = self.__class__
        fields = cls.model_fields
        dct = {}
        for name in self.model_fields_set.union(cls.api_transport_fields):
            field: TransportFieldInfo = fields[name]  # type: ignore
            typ = field.transport_type
            value = getattr(self, name)
            unparsed = typ.unparse_py(value, enc)
            # determine the field name for the output mapping
            alias = field.alias if by_alias else None
            name = alias if alias and by_alias else name
            # set the value
            dct[name] = unparsed
        return dct

    def to_dict(self, by_alias: bool = False) -> dict[str, Any]:
        """Return a dictionary representation of the ApiObject

        The return value will provide a mapping of transport field names to field
        values for the object.

        by_alias: If true, the return value will use JSON field alias names
        where defined, else the return value will use internal (Python) field
        names.
        """
        cls = self.__class__
        fields = cls.model_fields
        dct = {}
        dict_fields = cls.api_transport_fields.union(self.model_fields_set)
        for name in dict_fields:
            field: TransportFieldInfo = fields[name]  # type: ignore
            typ = field.transport_type
            value = getattr(self, name)
            if isinstance(typ, TransportValuesType):
                vlen = len(value)
                buf = [None] * vlen
                for n in range(0, vlen):
                    nth = value[n]
                    # Known limitation:
                    # this API does not support sequences of sequence, for transport object
                    if isinstance(nth, ApiObject):
                        out = nth.to_dict(by_alias)
                    else:
                        out = nth
                value = value.__class__(buf)
            elif isinstance(typ, ApiObject):
                value = value.to_dict(by_alias)

            alias = field.alias if by_alias else None
            name = alias if alias and by_alias else name
            # set the value
            dct[name] = value
        return dct

    #
    # Parser support methods
    #

    @classmethod
    def create_prototype(cls) -> Self:
        ## see parser - ModelBuilder.instance_prototype()
        return cls.__new__(cls)

    @classmethod
    def initialize_member_prototype(cls, key: str) -> "ApiObject":
        ## initialize a field member prototype from a concrete ApiObject class

        fields = cls.json_fields
        if key in fields:
            info: TransportFieldInfo = fields[key]
            mcls: "type[ApiObject]" = info.transport_type.storage_class
            return mcls.create_prototype()
        else:
            raise ValueError("Not a known field name", key, cls)

    @classmethod
    def finalize_prototype(cls, value: Self) -> Self:
        ## no further initialization, in the base class
        return value


## fxTrade v20 API uses enum values for denoting the implementation class
## of each abstract API class - e.g OrderType, TransactionType
Td = TypeVar("Td", bound=Enum)

TypesMap: TypeAlias = Union[dict[Td, type[Tobject]], Map[Td, type[Tobject]]]
"""Value type for designator/class mappings within an AbstractApiClass.

Once the defining class is finalized, the class' types map will be of an immutable
Map type"""


class AbstractApiClass(ApiClass):

    def __finalize_instance__(cls):
        if not cls.__finalized__:
            cls.types_map = Map(cls.types_map)
            return super().__finalize_instance__()

    def __new__(cls, cls_name: str,
                bases: tuple[type[Any]], namespace: dict[str, Any],
                designator_key: Optional[str] = None,
                designator_type: Optional[type[ApiObject]] = None):
        # fmt: off
        annotations = (namespace["__annotations__"] if "__annotations__" in namespace else {})
        # fmt: on

        if designator_key:
            namespace["designator_key"] = designator_key
            annotations["designator_key"] = ClassVar[str]

        if designator_type:
            namespace["designator_type"] = designator_type
            annotations["designator_type"] = ClassVar[type[designator_type]]  # type: ignore

        if "types_map" not in namespace:
            namespace["types_map"] = {}

        namespace["__annotations__"] = annotations

        return super().__new__(cls, cls_name, bases, namespace)


class AbstractApiObject(ApiObject, ABC, Generic[Td], metaclass=AbstractApiClass):
    ## for Request, Order, Transaction

    __finalize__: ClassVar[bool] = False
    """Finalization state flag for the AbstractApiObject class
    """

    types_map: ClassVar[TypesMap]
    """Designator/Types mapping for classes implementing the abstract API Object class.

    The types map will generally represent a mapping of each value of the class'
    `designator_type` to a correpsonding subclass of the class.

    ### Syntax and Finalization

    Before finalization, the `types_map` class field will be provided with a Python
    dict object. Subsequent of finalization, the `types_map` field will be provided
    with an immutable mapping.
    """

    designator_key: ClassVar[str]
    """Field name for the the designator key, within concrete implementations
    of the abstract API Object class
    """

    designator_type: ClassVar[Enum]
    """Enum type for the designator value, within concrete implementations of
    the abstract API Object class.
    """

    @classmethod
    def __init_subclass__(cls, *,
                          designator_key: Optional[str] = None,
                          designator_type: Optional[type[ApiObject]] = None,
                          **kw):
        super().__init_subclass__(**kw)
        if designator_key:
            cls.designator_key = designator_key
        if designator_type:
            cls.designator_type = designator_type
        if not (designator_key or designator_type or ABC in cls.__bases__):
            ## initialize an implementation class
            base = cls.get_abstract_base()
            key = base.designator_key
            serialize = set(cls.api_transport_fields)
            serialize.add(key)
            cls.api_transport_fields = frozenset(serialize)
            if hasattr(cls, key):
                hints = cls.__annotations__
                if key not in hints:
                    # fmt: off
                    raise ValueError("Subclass has no type hints for key attribute", key, cls, base)
                    # fmt: on
                key_hint = hints[key]
                if key_hint is designator_type:
                    raise ValueError("Subclass has unexpected designator_type binding", key_hint)
                literal_value = get_literal_value(key_hint)
                binding = {literal_value: cls}
                logger.debug("%s bind %r => %s", base.__name__, literal_value, cls.__name__)

                # register the subclass to the abstract base class
                base.bind_types(binding)
                # also register the subclass to the subclass' own types_map:
                cls.bind_types(binding)

    @classmethod
    def get_abstract_base(cls) -> type[Self]:
        for mcls in cls.__mro__:
            if AbstractApiObject in mcls.__bases__:
                return mcls
        raise ValueError("No abstract base class found", cls)

    @classmethod
    def bind_types(cls, types_map: TypesMap) -> TypesMap:
        ## returns: the updated types map
        ##
        ## known limitations: Not thread-safe for concurrent calls to
        ## bind_types() and finalize_prototype() or for updates to cls.types_map
        mapping = cls.types_map
        for typ, icls in types_map.items():
            assert isinstance(typ, cls.designator_type)
            assert issubclass(icls, cls)
            if typ in mapping:
                assert mapping[typ] is icls
            else:
                mapping[typ] = icls
        return map

    @classmethod
    def class_for_designator(cls, designator: Td) -> type[ApiObject]:
        ## return the implementation class defined for a given designator value
        if __debug__:
            if len(cls.types_map) is int(0):
                raise AssertionError("Types map is empty", cls)
            elif not designator:
                # fmt: off
                raise AssertionError("Abstract instance designator not provided", designator, cls.designator_key, cls)
        dtyp = cls.designator_type
        types_map = cls.types_map
        if designator.__class__ is dtyp and designator in types_map:
            return cls.types_map[designator]
        else:
            if isinstance(designator, bytes):
                designator = designator.decode()
            if designator in dtyp:
                # cast to enum
                denum = dtyp[designator]
                if denum in types_map:
                    return types_map[denum]
        raise ValueError("No class found for abstract instance designator", designator, cls)

    @classmethod
    def create_prototype(cls):
        # subsequently, see ApiObject.realize_map()
        return dict()

    ## should not be needed, given the realize_map() call before further parsing ...
    # @classmethod
    # def initialize_member_prototype(cls, key: str) -> dict:
    #     return dict()

    @classmethod
    def realize_map(cls, typ: Td, value: Mapping[str, Any]) -> Self:
        # utility method, [to be] applied when parsing with an abstract API type
        #
        # assumption: the server will present the designator key
        # for the abstract API object, before any key representing a
        # concrete field in the implementing class. Given this assumption,
        # the initial mapping value can be replaced with an actual object
        # instance, as soon as the designator key is parsed.
        #
        # This method would be applied to retrieve an object instance
        # for the intial mapping data. The parser may then  initialize
        # the new prototype instance, for each subsequent field parsed
        # from the server response
        proto_cls = cls.class_for_designator(typ)
        obj = proto_cls.__new__(proto_cls)
        json_fields = proto_cls.json_fields
        for name, fieldvalue in value.items():
            # assumption: each field value is of an appropriate storage
            # syntax for the abstract instance, requiring no further
            # parsing here
            #
            # using object.__setattr__ to avoid pydantic's model field validation
            #
            # Known Limitation: This assumes that the data being parsed is from a
            # trusted provider and would be valid for the containing model field
            if name in json_fields:
                info: TransportFieldInfo = json_fields[name]
                field_name = info.name
                parsed = info.transport_type.parse(fieldvalue)
                object.__setattr__ (obj, field_name, parsed)
                obj.model_fields_set.add(field_name)
            else:
                raise ValueError("Unknown JSON field", name, proto_cls)
        return obj

    @classmethod
    def finalize_prototype(cls, value: Union[dict, Self]) -> Self:
        inst = None

        if isinstance(value, dict):
            designator: Td = value.get(cls.designator_key)  # type:ignore
            model_cls = cls.class_for_designator(designator)
            if __debug__:
                if not model_cls:
                    # fmt: off
                    raise AssertionError("No model class found", designator, cls)
            inst = model_cls.__new__(model_cls)
            json_fields = model_cls.json_fields
            info: Optional[TransportFieldInfo] = None
            for key, unparsed_value in value.items():
                if key in json_fields:
                    info = json_fields[key]
                else:
                    raise ValueError("Unknown JSON field", key, model_cls)
                ttyp = info.transport_type
                parsed = ttyp.parse(unparsed_value)
                attr = info.name
                setattr(inst, attr, parsed)
        else:
            inst = value
        return super().finalize_prototype(inst)



__all__ = exporting(__name__, ..., "JsonTypesRepository")
