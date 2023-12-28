## Transport Types Repository

from enum import Enum
from collections.abc import Sequence, Mapping
from functools import partial
import immutables
import itertools

# import logging
from types import new_class
from typing import Any, Optional, Union
from typing_extensions import Self, TypeVar, get_args, get_origin


from ..util.typeref import get_type_class, TypeRef
from ..util.singleton_class import SingletonClass
from ..util.sequence_like import is_sequence_or_set_type

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

    def bind_transport_type(self, type: type[T_co], transport_type: TransportType[type[T_co], Any]):
        if self.__finalization_state__:
            raise ValueError("Repository is finalized", self)
        self.direct_types_map[type] = transport_type  # type: ignore[index]

    def bind_values_type(self, member_type: type[T_co], transport_type: TransportValuesType[type[T_co], Any]):
        if self.__finalization_state__:
            raise ValueError("Repository is finalized", self)
        self.member_types_map[member_type] = transport_type  # type: ignore[index]

    def bind_types(self, map: Mapping[type[T_co], TransportType[type[T_co], Any]]):
        if self.__finalization_state__:
            raise ValueError("Repository is finalized", self)
        for t, transport_t in map.items():
            self.bind_transport_type(t, transport_t)

    def init_enum_transport_type(self, etyp: type[Enum]) -> type[TransportEnumType]:
        assert issubclass(etyp, Enum), "Not an enum type"
        name = "Transport_" + etyp.__name__
        txtyp: type = None.__class__

        def init_ns(etyp: type, txtyp: type, ns: dict[str, Any]):
            ns["storage_type"] = etyp
            ns["storage_class"] = etyp
            ns['serialization_type'] = txtyp
            ns['serialization_class'] = txtyp

        nsfunc = partial(init_ns, etyp, txtyp)

        typ: TransportTypeClass
        if issubclass(etyp, str):
            txtyp = str
            typ = new_class(name, (TransportEnumStrType,), None, nsfunc)  # type: ignore[assignment]
        elif issubclass(etyp, int):
            txtyp = int
            typ = new_class(name, (TransportEnumIntType,), None, nsfunc)  # type: ignore[assignment]
        else:
            txtyp = str
            typ = new_class(name, (TransportEnumType,), None, nsfunc)  # type: ignore[assignment]

        typ.initialize_attrs()
        return typ

    def make_values_transport_type(self, decl: TypeRef, *,
                                   member_class: Optional[type] = None,
                                   storage_class: Optional[type] = None
                                   ) -> type[TransportValuesType]:
        ## create a values transport type, without binding the type
        ##
        member_cls = member_class or get_sequence_member_class(decl)
        if __debug__:
            if not isinstance(member_cls, type):
                raise AssertionError("member_class is not a type", member_cls)

        name = "Transport_" + member_cls.__name__ + "Values"
        member_transport_type = self.get_transport_type(member_cls)
        #
        # try to unparse any type alias wrapping in Python 3.10 and earlier
        # here list[int] is interpreted as an incomplete type object
        #
        origin = get_origin(storage_class)
        if origin is not None and is_sequence_or_set_type(origin):
            storage_class = origin
        # & cont
        storage_cls = storage_class or TransportValuesType.get_storage_class()

        def init_values_ns(member_transport_type, storage_cls, attrs: dict[str, Any]):
            attrs["member_transport_type"] = member_transport_type
            attrs["storage_type"] = storage_cls
            attrs["storage_class"] = storage_cls
            attrs["serialization_type"] = list
            attrs["serialization_class"] = list

        nsfunc = partial(init_values_ns, member_transport_type, storage_cls)

        cls: TransportTypeClass = new_class(name, (TransportValuesType,), None, nsfunc)  # type: ignore[assignment]
        cls.initialize_attrs()
        return cls

    def find_transport_type(self,
                            value_type: Union[type, TypeRef],
                            storage_class: Optional[type] = None
                            ) -> Optional[type[TransportType]]:
        ## applicable only for scalar values and transport object types ... maybe also enum types

        storage_cls = storage_class or get_type_class(value_type)
        if isinstance(storage_cls, TransportInterface):
            return self.direct_types_map.get(storage_cls, None)

        scls_origin = get_origin(storage_cls)

        if scls_origin is not None and is_sequence_or_set_type(scls_origin):
            # should be a sufficient type check for Python 3.10 and
            # earlier and for Python 3.11 and later, given the different
            # handling for e.g `list[int]` for Python releases in
            # the respective revision ranges.
            #
            # Python 3.11 introduces a generic typing for expressions
            # such as `list[int]` such that the object represented by
            # the expression is not a type.
            #
            # In Python 3.10 and earlier, `list[int]` is processed as
            # a type object. However, the type object will not be
            # initialized such a to be applicable as a first arg
            # for some tests with `issubclass()`, mainly as when the
            # second arg to issubclass() is a user-defined class.
            #
            # In either revision range: get_origin(list[int]) -> list
            # thus returning a class reference such that can be used
            # for the sequence type test, here.
            #
            # This has not been tested with complex type definitions
            #
            # At this time, get_sequence_member_class() itself
            # appears to be portable at least with Python 3.10 and later
            #
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
            if __debug__:
                if typ is None:
                    raise RuntimeError("'None' key for transport type", mapping[None])
            # Populate mro_map as a dictionary of mro index values
            # for each key type from `mapping` in which the storage_class
            # is a subclass of that key type and the key type is
            # present in the method resolution order for the type class.
            #
            # If the storage_class is a subclass of the key type, but
            # the key type is not present in the MRO for the storage
            # class, then the key type will be added to no_mro
            #
            # when the mro_map and no_mro collections are both
            # non-empty, values in mro_map will be preferred
            #
            # If more than one class is present in no_mro and no
            # classes are present in mro_map, raises ValueError
            #
            # If no classes are present in mro_map but a single class is
            # present in no_mro, returns the transport type for the class
            # in no_mro. This may be reached for an abstract class present
            # on the left hand side of the value-type-to-transport-type
            # mapping, such that the abstract type recognizes the storage
            # class as a subclass, while the abstract type is not present
            # in the method resolution order for the storage class - e.g for
            # some abstract base classes.
            #
            # When not any classes are present in mro_map or non_mro,
            # raises ValueError
            #
            # Subsequently, for any classes in mro_map, returns the
            # transport type for the nearest base class of the storage_class,
            # for nearness derived from the key class' position in the
            # method resolution order for the storage class
            #
            # The get_args test here is for how type aliases are handled
            # in Python 3.10 and earlier, such that a type aliwas will be
            # processed as a type but may fail as a first arg under issubclass()
            # when the second arg is a user-defined class.
            if get_args(storage_cls) is None and issubclass(storage_cls, typ):
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
                           value_type: Union[type, TypeRef],
                           storage_class: Optional[type] = None) -> TransportType:
        storage_cls: type = storage_class or get_type_class(value_type)
        if __debug__:
            if not storage_cls:
                raise AssertionError("No storage_class", value_type, storage_class)
        found = self.find_transport_type(value_type, storage_cls)
        if found:
            return found
        elif self.__finalization_state__:
            raise ValueError("Repository is finalized", self)
        elif issubclass(storage_cls, Enum):
            etyp = self.init_enum_transport_type(storage_cls)
            self.bind_transport_type(storage_cls, etyp)
            return etyp
        elif isinstance(storage_cls, TransportInterface):
            txtyp = new_class(storage_cls.__name__ + "_Transport", (storage_cls,))
            self.bind_transport_type(storage_cls, txtyp)
            return txtyp
        elif storage_cls is list or storage_cls is Sequence or is_sequence_or_set_type(storage_cls) or is_sequence_or_set_type(get_origin(storage_cls)):
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
