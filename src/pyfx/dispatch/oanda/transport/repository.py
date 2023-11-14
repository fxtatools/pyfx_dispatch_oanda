## Transport Types Repository

from enum import Enum
from collections import ChainMap
from collections.abc import Sequence, Mapping
import immutables
import itertools

# import logging
from types import new_class, NoneType
from typing import Any, Optional, Union, Self
from typing_extensions import TypeAlias, TypeVar


from ..util.typeref import get_type_class
from ..util.singleton_class import SingletonClass
from ..util.sequence_like import StdSequenceLike

from ..finalizable import Finalizable

from .transport_base import (
    TransportInterface,
    TransportType,
    TransportTypeClass,
    TransportValuesType,
    get_sequence_member_class,
)

from .transport_base import (
    TransportEnumType,
    TransportEnumStrType,
    TransportEnumIntType,
)

from ..util.naming import exporting


T_type = TypeVar("T_type", bound=type)


T_co = TypeVar("T_co", covariant=True)


class TransportRepositoryClass(SingletonClass[T_co]):
    pass


class TransportBaseRepository(Finalizable, metaclass=TransportRepositoryClass[Self]):
    __slots__ = "direct_types_map", "member_types_map" #, "__finalization_state__" #, "__finalized__"

    direct_types_map: Union[dict[type, type[TransportType]], Mapping[type, type[TransportType]]]
    """mapping of internal value types to transport types for non-sequence, non-set types

    This mapping will be immutable after the repository is finalized"""

    member_types_map: Union[dict[type, type[TransportValuesType]], Mapping[type, type[TransportValuesType]]]
    """mapping of Sequence and Set member types to values-typed transport types

    This mapping will be immutable after the repository is finalized"""

    @classmethod
    def initialize_singleton(cls):
        return cls()

    def __finalize_instance__(self):
        if self.__finalization_state__:
            return
        self.direct_types_map = immutables.Map(self.direct_types_map)
        self.member_types_map = immutables.Map(self.member_types_map)
        for cls, typ in itertools.chain(self.direct_types_map.items(), self.member_types_map.items()):
            if hasattr(cls, "__finalize__"):
                cls: Finalizable
                cls.__finalize_instance__()
            if hasattr(typ, "__finalize__"):
                typ: TransportType
                typ.__finalize_instance__()
        super().__finalize_instance__()

    def __init__(self, **bindings):
        self.__finalization_state__ = False
        self.direct_types_map = dict()
        self.member_types_map = dict()
        self.bind_types(bindings)

    def bind_transport_type(self, type: T_type, transport_type: type[TransportType[T_type, Any]]):
        if self.__finalization_state__:
            raise ValueError("Repository is finalized", self)
        self.direct_types_map[type] = transport_type  # type: ignore[index]

    def bind_values_type(self, member_type: type[T_type], transport_type: type[TransportValuesType[T_type, Any]]):
        if self.__finalization_state__:
            raise ValueError("Repository is finalized", self)
        self.member_types_map[member_type] = transport_type  # type: ignore[index]

    def bind_types(self, map: Mapping[T_type, type[TransportType[T_type, Any]]]):
        if self.__finalization_state__:
            raise ValueError("Repository is finalized", self)
        for t, transport_t in map.items():
            self.bind_transport_type(t, transport_t)

    def init_enum_transport_type(self, etyp: type[Enum]) -> type[TransportEnumType]:
        assert issubclass(etyp, Enum), "Not an enum type"
        name = "Transport_" + etyp.__name__
        txtyp: type = NoneType

        def init_ns(ns: dict[str, Any]):
            nonlocal etyp, txtyp
            ns["storage_type"] = etyp
            ns["storage_class"] = etyp
            ns['serialization_type'] = txtyp
            ns['serialization_class'] = txtyp

        typ: TransportTypeClass
        if issubclass(etyp, str):
            txtyp = str
            typ = new_class(name, (TransportEnumStrType,), None, init_ns)  # type: ignore[assignment]
        elif issubclass(etyp, int):
            txtyp = int
            typ = new_class(name, (TransportEnumIntType,), None, init_ns)  # type: ignore[assignment]
        else:
            txtyp = str
            typ = new_class(name, (TransportEnumType,), None, init_ns)  # type: ignore[assignment]

        typ.initialize_attrs()
        return typ

    def make_values_transport_type(self, decl: TypeAlias, *,
                                   member_class: Optional[type] = None,
                                   storage_class: Optional[type] = None
                                   ) -> type[TransportValuesType]:
        member_cls = member_class or get_sequence_member_class(decl)
        if __debug__:
            if not isinstance(member_cls, type):
                raise AssertionError("member_class is not a type", member_cls)

        name = "Transport_" + member_cls.__name__ + "Values"
        member_transport_type = self.get_transport_type(member_cls)
        storage_cls = storage_class or TransportValuesType.get_storage_class()

        def init_values_ns(attrs: dict[str, Any]):
            nonlocal member_transport_type, storage_cls
            attrs["member_transport_type"] = member_transport_type
            attrs["storage_type"] = storage_cls
            attrs["storage_class"] = storage_cls
            attrs["serialization_type"] = list
            attrs["serialization_class"] = list

        cls: TransportTypeClass = new_class(name, (TransportValuesType,), None, init_values_ns)  # type: ignore[assignment]
        cls.initialize_attrs()
        return cls

    def find_transport_type(self,
                            value_type: Union[type, TypeAlias],
                            storage_class: Optional[type] = None
                            ) -> Optional[type[TransportType]]:

        storage_cls = storage_class or get_type_class(value_type)

        if issubclass(storage_cls, TransportInterface):
            return storage_cls
        elif isinstance(value_type, TransportInterface):
            # supporting a value type using a TransportType metclass,
            # e.g TradeId
            return value_type
        elif issubclass(storage_cls, StdSequenceLike):
            member_cls = get_sequence_member_class(value_type)
            return self.member_types_map.get(member_cls, None)

        mapping = self.direct_types_map

        if issubclass(storage_cls, Enum):
            return mapping.get(storage_cls, None)

        mro_map = {}
        no_mro: list[type] = []
        vmro: tuple[type, ...] = storage_cls.__mro__

        bound = mapping.get(storage_cls, None)
        if bound is not None:
            return bound

        for typ in mapping.keys():
            if issubclass(storage_cls, typ):
                try:
                    idx = vmro.index(typ)
                    mro_map[idx] = typ
                except ValueError:
                    ## typ is not present in the MRO for the storage_class,
                    ## though the storage_class is a subclass of typ
                    no_mro.append(typ)

        if len(mro_map) is int(0):
            if len(no_mro) is int(0):
                return None
            elif len(no_mro) > 1:
                # no matching type was found by method resolution order, and more than one
                # matching type was found by way of subclass test
                #
                # Outside of the storage class' method resolution order, there may be no
                # deterministic way to infer an ordering for class precedence, given more
                # than one matching type definition
                #
                # This may be reached if a transport type is defined for more than one
                # effective abstract superclass of the provided storage class
                #
                # fmt: off
                raise ValueError("Ambiguous transport type for storage class", no_mro, storage_cls)
                # fmt: on
            else:
                inferred_type = no_mro[0]
                return mapping[inferred_type]
        else:
            # return the transport type for a base class of the original storage_class,
            # selecting what whould be the "nearest" class per method resolution order
            nearest = sorted(mro_map.items(), key=lambda item: item[0])
            cls = nearest[0][1]
            return mapping[cls]

    def get_transport_type(self,
                           value_type: Union[type, TypeAlias],
                           storage_class: Optional[type] = None) -> TransportType:
        storage_cls: type = storage_class or get_type_class(value_type)
        found = self.find_transport_type(value_type, storage_cls)
        if found:
            return found
        elif self.__finalization_state__:
            raise ValueError("Repository is finalized", self)
        elif issubclass(storage_cls, Enum):
            etyp = self.init_enum_transport_type(storage_cls)
            self.bind_transport_type(storage_cls, etyp)
            return etyp
        elif storage_class is list or storage_cls is Sequence or issubclass(storage_cls, StdSequenceLike):
            eltcls = get_sequence_member_class(value_type)
            eltcls_match = self.member_types_map.get(eltcls, False)
            if eltcls_match is not False:
                return eltcls_match
            vtyp = self.make_values_transport_type(value_type, storage_class=storage_cls)
            self.bind_values_type(vtyp.member_transport_type.storage_class, vtyp)
            return vtyp
        else:
            raise ValueError("No transport type could be inferred", value_type, storage_cls)


__all__ = tuple(exporting(__name__, ...))
