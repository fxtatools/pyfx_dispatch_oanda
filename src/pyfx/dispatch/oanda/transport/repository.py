## Transport Types Repository

from json import JSONEncoder
from enum import Enum
from collections.abc import Sequence, Set, Mapping
from datetime import datetime

# import logging
from numpy import datetime64, double
from pandas import Timestamp
from types import new_class, MappingProxyType, NoneType
from typing import Any, Generic, Optional, Union
from typing_extensions import TypeAlias, TypeVar

from ..util.typeref import get_type_class

from .transport_base import (
    TransportFieldInfo,
    TransportType,
    TransportValues,
    get_sequence_member_class,
)
from .data import ApiObject, AbstractApiClass
from .transport_types import (
    TransportNone,
    TransportBool,
    TransportTimestamp,
    TransportInt,
    TransportFloatStr,
    TransportStr,
    TransportEnum,
    TransportEnumString,
    TransportEnumInt,
)

from ..util.naming import exporting


SEQUENCE_LIKE: tuple[type, ...] = (list, tuple, set,)


class TransportTypesRepository:
    @property
    def direct_types_map(self) -> Mapping[type, TransportType]:
        """mapping of internal value types to transport types for non-sequence, non-set types"""
        return self._direct_types_map

    @property
    def member_types_map(self) -> Mapping[type, TransportType]:
        """mapping of Sequence and Set member types to values-typed transport types"""
        return self._member_types_map

    @property
    def finalized(self) -> bool:
        return self._finalized

    def finalize(self):
        if self._finalized:
            return
        self._direct_types_map = MappingProxyType(self._direct_types_map)
        self._member_types_map = MappingProxyType(self._member_types_map)
        self._finalized = True

    def __init__(self, **bindings):
        self._finalized = False
        self._direct_types_map = dict()
        self._member_types_map = dict()
        self.bind_map(bindings)

    def bind(self, type: type[Any], transport_type: TransportType):
        self.direct_types_map[type] = transport_type

    def bind_map(self, map: Mapping[type, TransportType]):
        for t, transport_t in map.items():
            self.bind(t, transport_t)

    def make_object_transport_type(self, value_type: type[ApiObject]) -> TransportType:
        assert issubclass(value_type, ApiObject), "Not an ApiObject type"
        name = "Transport_" + value_type.__name__
        typ = new_class(name, (TransportObject[value_type, Mapping[str, Any]],))
        typ.initialize_attrs()
        typ.storage_class = value_type
        self.direct_types_map[value_type] = typ
        return typ

    def make_enum_transport_type(self, etyp: type[Enum]) -> TransportType:
        name = "Transport_" + etyp.__name__
        assert issubclass(etyp, Enum), "Not an enum type"
        styp = None

        def init_ns(ns: Mapping[str, Any]):
            nonlocal etyp, styp
            ns["storage_class"] = etyp
            ns["storage_type"] = etyp

        if issubclass(etyp, str):
            styp = str
            typ = new_class(name, (TransportEnumString[etyp, str],), None, init_ns)
        elif issubclass(etyp, int):
            styp = int
            typ = new_class(name, (TransportEnumInt[etyp, int],), None, init_ns)
        else:
            styp = str
            typ = new_class(name, (TransportEnum[etyp, str],), None, init_ns)
        self.direct_types_map[etyp] = typ
        typ.initialize_attrs()
        return typ

    def make_values_transport_type(
        self,
        decl: TypeAlias,
        member_class: type,
    ) -> TransportType:
        if __debug__:
            if not isinstance(member_class, type):
                raise AssertionError("member_class is not a type", member_class)
        name = "Transport_" + member_class.__name__ + "Values"

        member_transport_type = self.get_transport_type(member_class)

        storage_cls = TransportValues.get_storage_class()

        def init_values_ns(attrs: Mapping[str, Any]):
            nonlocal member_class
            attrs["member_transport_type"] = member_transport_type
            attrs["storage_type"] = storage_cls
            attrs["storage_class"] = storage_cls
            ## using the list representation, for JSON lists
            attrs["serialization_class"] = list
            attrs["serialization_type"] = list

        cls = new_class(
            name,
            (TransportValues[member_class, member_class],),
            {"member_class": member_transport_type, "storage_class": storage_cls},
            init_values_ns,
        )
        cls.initialize_attrs()
        return cls

    def get_values_transport_type(self, # fmt: off
                                  value_type: Union[type, TypeAlias], *,
                                  type_class: Optional[type] = None,
                                  no_define: bool = False,
                                  ) -> type[TransportValues]:
        # fmt: on
        if __debug__:
            _type_class = type_class if type_class else get_type_class(value_type)
            if not issubclass(_type_class, Sequence):
                raise ValueError("Not a sequence type", _type_class)
        member_type = get_sequence_member_class(value_type)
        vmap = self._member_types_map
        if member_type in vmap:
            return vmap[member_type]
        else:
            typ = self.make_values_transport_type(value_type, member_type)
            vmap[member_type] = typ
            return typ

    def get_transport_type(self, # fmt: off
                           value_type: Union[type, TypeAlias]
                           ) -> type[TransportType]:
        ## compute the transport type for a provided value type
        ## application: mainly for TransportFieldInfo initialization
        ##
        ## raises ValueError if no transport type is declared and none can be inferred,
        ## or if a non-type value_type is provided, such that no concrete type class
        ## can be inferred
        type_class = (value_type if isinstance(value_type, type) else get_type_class(value_type))
        # fmt: on
        mapping = self.direct_types_map
        if isinstance(type_class, TransportType):
            return type_class
        elif not issubclass(type_class, Enum) and (
            type_class is Sequence or issubclass(type_class, SEQUENCE_LIKE)
        ):
            return self.get_values_transport_type(value_type, type_class=type_class)
        elif issubclass(type_class, ApiObject):
            # Create a new transport type for the ApiObject class
            new_type = self.make_object_transport_type(type_class)
            # register and return the new transport type
            mapping[type_class] = new_type
            return new_type
        elif type_class in mapping:
            return mapping[type_class]
        elif issubclass(type_class, Enum):
            return self.make_enum_transport_type(type_class)
        else:
            mro_map = {}
            no_mro = []
            vmro: tuple = type_class.__mro__
            for t, transport_t in mapping.items():
                # Populate mro_map as a dictionary of mro index values
                # for each key type from `mapping` in which the type_class
                # is a subclass of that key type and the key type is
                # present in the method resolution order for the type class.
                #
                # If the type class is a subclass of the key type, but
                # the key type is not present in the MRO for the type
                # class, then the key type will be added to no_mro
                #
                # when the mro_map and no_mro collections are both
                # non-empty, values in mro_map will be preferred
                #
                # If more than one class is present in no_mro and no
                # classes are present in mro_map, raises ValueError
                #
                # If no classes are present in mro_map but a single class is
                # present in no_mro, returns the transport type for that class.
                # This may be reached, theoretically, for an abstract type
                # present on the left hand side of the value-type-to-transport-
                # type mapping.
                #
                # When not any classes are present in mro_map or non_mro,
                # raises ValueError
                #
                # Subsequently, for any classes in mro_map, returns the
                # transport type for the nearest base class of the type_class
                if issubclass(type_class, t):
                    try:
                        idx = vmro.index(t)
                        mro_map[idx] = t
                    except ValueError:
                        ## t is not present in the MRO for type_class,
                        ## though the type_class is a subclass of t
                        no_mro.append(t)

            if len(mro_map) is int(0):
                if len(no_mro) is int(0):
                    # fmt: off
                    raise ValueError("No transport type declared, none inferred", type_class)
                    # fmt: on
                else:
                    # no matching type was found by method resolution order, though
                    # matching type was found by way of subclass test
                    #
                    # This will allow for at most one matching class. Outside of
                    # method resolution order, there may be no deterministic way to
                    # infer an ordering for class precedence.
                    last = no_mro[-1]
                    transport_t = mapping[last]
                    if len(no_mro) > 1:
                        # fmt: off
                        raise ValueError("Ambiguous field type mapping", value_type, no_mro)
                        # fmt: on
                    return transport_t
            else:
                # return the transport type for a base class of the original type_class,
                # selecting what should be the "nearest" class per method resolution order
                nearest = sorted(mro_map.items(), key=lambda item: item[0])
                cls = nearest[0][1]
                return mapping[cls]


JsonTypesRepository: TransportTypesRepository = TransportTypesRepository()
JsonTypesRepository.bind_map(
    {
        ## initialize transport types for scalar values
        bool: TransportBool,
        NoneType: TransportNone,
        str: TransportStr,
        int: TransportInt,
        float: TransportFloatStr,
        double: TransportFloatStr,
        datetime: TransportTimestamp,
        datetime64: TransportTimestamp,
        Timestamp: TransportTimestamp,
    }
)


class ApiJsonEncoder(JSONEncoder):
    """JSON encoder for API Object classes"""

    def __init__(self):
        super().__init__(ensure_ascii=False, check_circular=False)

    def default(self, pyobj: Any) -> Any:
        ocls = pyobj.__class__
        typ: TransportType = ocls if isinstance(ocls, TransportType) else JsonTypesRepository.get_transport_type(ocls)  # type: ignore
        rslt = typ.unparse(pyobj, self)
        return rslt


Tobject = TypeVar("Tobject", bound=ApiObject)


class TransportObject(TransportType[Tobject, Mapping[str, Any]], Generic[Tobject]):
    @classmethod
    def parse(cls, unparsed: Union[ApiObject, Mapping[str, Any]]) -> Tobject:
        if isinstance(unparsed, cls.storage_class):
            # handle partial deserialization under the initial parse from stream
            return unparsed  # type: ignore
        else:
            assert isinstance(unparsed, Mapping), "Not a mapping value"
            model_cls: type[ApiObject] = cls.storage_class
            if isinstance(model_cls, AbstractApiClass):
                key = model_cls.designator_key
                designator = unparsed[key]
                model_cls = model_cls.class_for_designator(designator)
            fields = model_cls.api_fields
            info = None
            inst = model_cls.__new__(model_cls)
            for key, inteval in unparsed.items():
                if key in fields:
                    info = fields[key]
                else:
                    raise ValueError("Unknown field", key, model_cls)
                ttyp = info.transport_type
                parsed = ttyp.parse(inteval)
                attr = info.field_name
                setattr(inst, attr, parsed)
                # object.__setattr__(inst, attr, parsed)
            return inst

    @classmethod
    def unparse(cls, o: Tobject, encoder: ApiJsonEncoder) -> Mapping[str, Any]:
        m = dict()
        cls = o.__class__
        fields = cls.model_fields
        json_names = cls.json_field_names
        for f in o.__pydantic_fields_set__.union(cls.api_transport_fields):
            field_info: TransportFieldInfo = fields[f]
            if __debug__:
                if not isinstance(field_info, TransportFieldInfo):
                    raise AssertionError("Not a TransportFieldInfo", field_info)
            # name: str = json_names[f]
            name: str = json_names.get(f)
            transport_type: TransportType = field_info.transport_type
            val = getattr(o, f)
            if val is None:
                m[name] = "null"
            else:
                val = transport_type.unparse(val, encoder)
                # print("ENC %r %r" % (name, val,))
                m[name] = val
        return m


__all__ = tuple(exporting(__name__, ..., "JsonTypesRepository"))
