## base types for transport data model

from collections.abc import Mapping
# from reprlib import repr
from json import JSONEncoder
import logging
from pydantic import ConfigDict, BaseModel
from pydantic.fields import PydanticUndefined
from pydantic._internal._model_construction import ModelMetaclass
import sys
from types import MappingProxyType
from typing import Any, Generic, Optional, Tuple, TypeAlias, Union
from typing_extensions import ClassVar, Self, TypeVar, TypeAlias, Union, get_type_hints

from ..util.typeref import get_type_class, get_literal_value

from ..util.naming import exporting

from .transport_base import TransportFieldInfo, TransportTypeInfer, TransportType, TransportValues

logger = logging.getLogger(__name__)

FieldName: TypeAlias = str


class ApiClass(ModelMetaclass):

    api_fields: MappingProxyType[str, TransportFieldInfo]
    '''Mapping of instance field names and alias JSON field names to field
       information objects'''

    json_field_names: MappingProxyType[str, str]
    '''Mapping of each instance field name to its JSON field name'''

    always_serialize_fields: type[frozenset[str]]
    '''
    Field names for fields that should always be serialized, whether or not directly set
    within an instance.

    Each field in this frozen set must be either set or provided with a default value,
    in each serialized instance.
    '''

    @classmethod
    def default_model_config(cls):
        return ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, validate_assignment=False,
                          alias_priority=2
                          )

    @staticmethod
    def __new__(cls, cls_name: str, bases: Tuple[type[Any]], namespace: Mapping[str, Any]):
        overrides = dict()

        if "model_config" not in namespace:
            overrides['model_config'] = cls.default_model_config()

        if "api_fields" not in namespace:
            ## if a api_fields arg is provided in the dict component to __new__
            ## then it should be provided as a mutable mapping of string field
            ## names and field alias names, each mapped to a FieldInfo object.
            ## The value will be replaced with an immutable mapping, below.
            overrides["api_fields"] = dict()
        if "json_field_names" not in namespace:
            overrides["json_field_names"] = dict()

        serialize = set(namespace.get("always_serialize_fields", ()))
        for base in bases:
            if hasattr(base, "always_serialize_fields"):
                serialize = serialize.union(base.always_serialize_fields)
        serialize = frozenset(serialize)
        overrides["always_serialize_fields"] = serialize

        ## add class variables to annotations
        annotations = namespace["__annotations__"] if "__annotations__" in namespace else {}
        if "api_fields" not in annotations:
            annotations["api_fields"] = ClassVar[MappingProxyType[str, TransportFieldInfo]]
        if "json_field_names" not in annotations:
            annotations["json_field_names"] = ClassVar[MappingProxyType[str, str]]
        overrides["__annotations__"] = annotations

        namespace.update(overrides)
        new_cls: Self = super().__new__(cls, cls_name, bases, namespace)

        repository = sys.modules[__package__].__dict__.get("JsonTypesRepository")
        if __debug__:
            if not repository:
                logger.debug("JSON Types Repository not found when initiaizliaing %s", new_cls.__name__)

        hints = get_type_hints(new_cls)
        api_fields = new_cls.api_fields
        json_field_names = new_cls.json_field_names
        serialize_post = set(new_cls.always_serialize_fields)

        # this assumes that the class' type hints are all resolvable at the time when the ApiClass[ApiObject] class is initialized.

        for field_name, info in new_cls.model_fields.items():
            ## update the name_map
            api_fields[field_name] = info
            alias = info.alias
            if alias:
                api_fields[alias] = info
                json_field_names[field_name] = alias
            else:
                json_field_names[field_name] = field_name

            if isinstance(info, TransportFieldInfo):
                if not hasattr(info, "defining_class"):
                    info.defining_class = new_cls
                if not hasattr(info, "field_name"):
                    info.field_name = field_name

                default = info.get_default()
                if default and default is not PydanticUndefined:
                    ## ensure fields with non-None default values will be serialized
                    serialize_post.add(field_name)

                ttype = info.transport_type
                if __debug__:
                    if not isinstance(ttype, type):
                        raise AssertionError("Not a type", ttype, info, cls)
                if issubclass(ttype, TransportTypeInfer) or not ttype:
                    field_hint = hints.get(field_name)
                    field_type = get_type_class(field_hint)
                    if isinstance(field_type, TransportType):
                        # the field's concrete type is a transport type
                        #
                        # generally for types defined in ..common_types
                        field_type: TransportType
                        info.transport_type = field_type
                        info.storage_class = field_type.storage_class
                    elif field_hint:
                        typ = repository.get_transport_type(field_hint)
                        if not typ:
                            raise ValueError("Repository produced a null transport type", field_hint, field_name, cls)
                        info.transport_type = typ
                        info.storage_class = get_type_class(field_hint)
                    else:
                        # assumption: the new_cls may represent a generalized type
                        pass
        new_cls.api_fields = MappingProxyType(api_fields)
        new_cls.json_field_names = MappingProxyType(json_field_names)
        new_cls.always_serialize_fields = frozenset(serialize_post)

        if repository:
            ## preload the transport type storage, by side effect
            repository.get_transport_type(new_cls)

        return new_cls


class ApiObject(BaseModel, metaclass=ApiClass):

    validate_fields: ClassVar[bool] = __debug__
    always_serialize_fields: ClassVar[frozenset[str]]

    @staticmethod
    def __new__(cls, **kw):
        """construct an ApiObject without field validation

        Known Limitations:
        - The new instance will not have been validated for required model fields
        - Default field values will not have been set in the new instance. This
          limitation may be at least partly mitigated for default field value access,
          with the  definition of `ApiObject.__getattr__()`. No similar extension
          method has been defined for `hasattr()`"""
        inst = super().__new__(cls)
        object.__setattr__(inst, "__pydantic_extra__", None)
        for arg, value in kw.items():
            object.__setattr__(inst, arg, value)
        fields_kw = set(cls.model_fields.keys()).intersection(set(kw.keys()))
        object.__setattr__(inst, "__pydantic_fields_set__", fields_kw)
        return inst

    @classmethod
    def new(cls, **kw):
        """construct an ApiObject with field validation"""
        return cls.model_construct(**kw)

    def __hash__(self) -> int:
        s = {}
        for field in self.__pydantic_fields_set__.union(self.__class__.always_serialize_fields):
            t = (field, hash(getattr(self, field)),)
            s.add(t)
        return hash(frozenset(s))

    def __eq__(self, other) -> bool:
        # defined mainly for application under tests.
        #
        # To be __eq__ in this implementation:
        # - self and other must be of the same class
        # - the same fields must have been set in self and other,
        #   for the set of fields recorded in __pydantic_fields_set__
        # - each value on each set field must be __eq__ for each
        #   instance
        #
        # On event of error, this will dispatch generally to
        # object.__eq__() which may then apply an 'is' test
        # for object equivalence
        try:
            if self.__class__ is not other.__class__:
                return False
            fields = self.__pydantic_fields_set__.union(self.__class__.always_serialize_fields)
            for f in fields:
                if getattr(self, f) != getattr(other, f):
                    return False
            return True
        except Exception:
            return super().__eq__(other)

    def to_str(self) -> str:
        """Returns a string representation of the object, without field alias names"""
        return self.model_dump(by_alias=False, exclude_none=True, exclude_unset=False)

    def to_json_str(self, encoder: JSONEncoder) -> str:
        """Returns a JSON string representation of the object, using field alias names

        See also: ApiJsonEncoder"""
        ## repeated occurrence: ValueError: Circular reference detected
        return encoder.encode(self)
        ## this does not deserialize SecretStr values correctly - it is a type-based issue, not of any one field
        # return self.model_dump_json(by_alias=True)

    def to_json_bytes(self) -> bytes:
        return self.to_json_str().encode()

    @classmethod
    def from_json(cls, json_str: str, context: Optional[Mapping[str, Any]] = None) -> Self:
        """Creates an instance of the ApiObject class from a JSON string"""
        return cls.model_validate_json(json_str, context=context)

    @classmethod
    def from_dict(cls, obj: Optional[Union[Mapping[str, Any], Self]]) -> Self:
        """Creates an instance of the ApiObject class from a mapping value"""
        return cls.model_validate(obj)

    def to_transport_dict(self, by_alias: bool = False, encoder: Optional[JSONEncoder] = None):
        """Returns a dictionary representation of the object encoded in tranport syntax for each value, optionally using field alias names"""
        enc = encoder if encoder else JSONEncoder(check_circular=False, ensure_ascii=False)
        cls = self.__class__
        fields = cls.model_fields
        dct = {}
        for field_name in self.model_fields_set.union(cls.always_serialize_fields):
            field: TransportFieldInfo = fields[field_name]
            typ = field.transport_type
            value = getattr(self, field_name)
            unparsed = typ.unparse(value, encoder)  # TBD storing the unparsed value here, or the internal value here
            # determine the field name for the output mapping
            alias = field.alias if by_alias else None
            name = alias if alias and by_alias else field_name
            # set the value
            dct[name] = unparsed
        return dct

    def to_dict(self, by_alias: bool = False):
        """Returns a dictionary representation of field names and internal field values for the object,
        optionally using field alias names"""
        cls = self.__class__
        fields = cls.model_fields
        dct = {}
        for field_name in self.model_fields_set.union(cls.always_serialize_fields):
            field: TransportFieldInfo = fields[field_name]
            typ = field.transport_type
            value = getattr(self, field_name)
            if isinstance(typ, TransportValues):
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
            name = alias if alias and by_alias else field_name
            # set the value
            dct[name] = value
        return dct

    def __getattr__(self, attr: str):
        """If the `key` name denotes a model field for the instance not present in
        `self.model_fields_set`, returns the default value for that field. Else,
        returns the value from the superclass' `__getattr__()` function

        If the `key` name denotes a required model field and the field is unset in
        this instance, raises AttributeError.
        """
        fields = self.__class__.model_fields
        if attr in fields:
            if attr in self.model_fields_set:
                return super().__getattr__(attr)
            else:
                field = fields[attr]
                default = field.get_default()
                if default is PydanticUndefined:
                    raise AttributeError("Field is unset and has no default value", attr)
                else:
                    return default
        else:
            return super().__getattr__(attr)

    def __getitem__(self, key: str, assume_model: bool = False) -> Any:
        """Set the value for the attribute `key`, if `key` denotes a model field.

        This function provides support for a subscript syntax in accessing model
        attributes of an ApiObject.

        For a `key` not matching a model field for the instance, raises KeyError."""
        model_fields = self.__class__.model_fields
        if assume_model or key in model_fields:
            return getattr(self, key)
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
        if assume_model or key in self.__class__.model_fields:
            return setattr(self, key, value)
        else:
            raise KeyError("Model field not found", key)

    def __delitem__(self, key: str, assume_model: bool = False) -> Any:
        """remove the provided key from the set of "set" fields for the instance
        and set the default value for the attribute named in `key`.

        This function provides support for a subscript syntax in effectively
        deleting a model attribute from an ApiObject.

        For a `key` not matching a model field for the instance, raises KeyError.

        If no default value is avaialble, raises KeyError before modifying the instance.

        This function assumes that the `key` is provided in the Python syntax for the model
        field, rather than as using a model field alias name.

        Known Limitations:
        - Not thread-safe for concurrent read and modification of model fields"""
        fields = self.__class__.model_fields
        if assume_model or key in fields:
            field = fields[key]
            default = field.get_default()
            if default is PydanticUndefined:
                raise KeyError("Unable to unset a field with no default value", key)
            setattr(self, key, default)
            self.__pydantic_fields_set__.remove(key)
        else:
            raise KeyError("Model field not found", key)

    def __repr__(self, cache: Optional[list] = None):
        return self.__class__.__qualname__ + "(" + ", ".join({field + "=" + repr(getattr(self, field)) for field in self.model_fields_set}) + ")"

    def __str__(self):
        return self.__class__.__qualname__ + "(" + ", ".join({field + "=" + str(getattr(self, field)) for field in self.model_fields_set}) + ")"

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

        fields = cls.api_fields
        if key in fields:
            info: TransportFieldInfo = fields[key]
            mcls: "type[ApiObject]" = info.transport_type.storage_class
            return mcls.initialize_prototype()
        else:
            raise ValueError("Not a known field name", key, cls)

    @classmethod
    def finalize_prototype(cls, value: Self) -> Self:
        ## no further instance initialization to perform, generally
        return value


Td = TypeVar("Td", bound=ApiObject)

TypesMap: TypeAlias = Mapping[Td, type[Self]]


class AbstractApiClass(ApiClass):
    @staticmethod
    def __new__(cls, cls_name: str, bases: Tuple[type[Any]], namespace: Mapping[str, Any],
                designator_key: Optional[str] = None,
                designator_type: Optional[type[ApiObject]] = None):

        annotations = namespace["__annotations__"] if "__annotations__" in namespace else {}

        if designator_key:
            namespace['designator_key'] = designator_key
            annotations['designator_key'] = ClassVar[str]

        if designator_type:
            namespace['designator_type'] = designator_type
            annotations['designator_type'] = ClassVar[type[designator_type]]

        if 'types_map' not in namespace:
            namespace['types_map'] = {}

        namespace["__annotations__"] = annotations

        return super().__new__(cls, cls_name, bases, namespace)


class AbstractApiObject (ApiObject, Generic[Td], metaclass=AbstractApiClass):
    ## for Request, Order, Transaction

    types_map: ClassVar[TypesMap]
    designator_key: ClassVar[str]
    designator_type: ClassVar[type[ApiObject]]

    @classmethod
    def __init_subclass__(cls, *args, **kw):
        super().__init_subclass__(*args, **kw)
        if AbstractApiObject not in cls.__bases__:
            base = cls.get_abstract_base()
            key = base.designator_key
            serialize = set(cls.always_serialize_fields)
            serialize.add(key)
            cls.always_serialize_fields = frozenset(serialize)
            if hasattr(cls, key):
                hints = cls.__annotations__
                if key not in hints:
                    raise ValueError("Subclass has no type hints for key attribute", key, cls, base)
                key_hint = hints[key]
                if key_hint is cls.designator_type:
                    # an intermediate abstract class may not have provided a binding
                    # for the designator key - not an error
                    return
                literal_value = get_literal_value(key_hint)
                binding = {literal_value: cls}
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
        ## bind_types() and finalize_prototype()
        map = cls.types_map
        map.update(types_map)
        # map = MappingProxyType(map)
        cls.types_map = map
        return map

    @classmethod
    def class_for_designator(cls, designator: Td) -> type[Self]:
        ## of course the types map is empty for a concrete subclass of the abstract base class....
        ##
        ## TBD mapping from each such concrete class to a single abstract base class
        if __debug__:
            if len(cls.types_map) is int(0):
                raise AssertionError("Types map is empty", cls)
            elif not designator:
                raise AssertionError("Abstract instance designator not provided", designator, cls.designator_key, cls)
        if designator in cls.types_map:
            return cls.types_map[designator]
        else:
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
        proto = proto_cls.__new__(proto_cls)
        for field, fieldvalue in value.items():
            # assumption: each field value is of an appropriate storage
            # syntax for the abstract instance, requiring no further
            # parsing here
            #
            # using object.__setattr__ to avoid pydantic's model field validation
            #
            # Known Limitation: This assumes that the data being parsed is from a
            # trusted provider and would be valid for the containing model field
            object.__setattr__(proto, field, fieldvalue)
            proto.model_fields_set.add(field)
        return proto

    @classmethod
    def finalize_prototype(cls, value: Union[dict, Self]) -> Self:
        inst = None


        if isinstance(value, dict):
            designator = value.get(cls.designator_key)
            model_cls = cls.class_for_designator(designator)
            if __debug__:
                if not model_cls:
                    raise AssertionError("No model class found", designator, cls)
            inst = model_cls.__new__(model_cls)
            fields = model_cls.api_fields
            info = None
            for key, inteval in value.items():
                if key in fields:
                    info: TransportFieldInfo = fields[key]
                else:
                    raise ValueError("Unknown field", key, model_cls)
                ttyp = info.transport_type
                parsed = ttyp.parse(inteval)
                attr = info.field_name
                setattr(inst, attr, parsed)
        else:
            inst = value
        return super().finalize_prototype(inst)


__all__ = exporting(__name__, ...)
