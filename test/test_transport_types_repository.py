## Unit tests for Transport Types Repository

from abc import ABC
from collections.abc import Sequence
from pandas import Timestamp
from typing import Iterator

from assertpy import assert_that  # type: ignore[import-untyped]

from pyfx.dispatch.oanda.test import ComponentTest, run_tests
from pyfx.dispatch.oanda.transport.data import ApiObject, TransportObjectType
from pyfx.dispatch.oanda.transport.repository import TransportBaseRepository
from pyfx.dispatch.oanda.transport.transport_base import TransportBoolType, TransportIntType, TransportStrType, TransportValuesType
from pyfx.dispatch.oanda.transport.transport_base import TransportTimestampType


def effective_subclasses(cls: type) -> Iterator[type]:
    assert isinstance(cls, type), "Not a type"
    for scls in cls.__subclasses__():
        yield scls
        yield from effective_subclasses(scls)


def implementation_classes(cls: type) -> Iterator[type]:
    for scls in {cls for cls in effective_subclasses(cls)}:
        if len(scls.__bases__) is int(0) and ABC not in scls.__bases__:
            yield scls


class TestDataModel(ComponentTest):
    """Unit tests for Transport Types Repository"""

    def test_transport_type_get(self):
        repository = TransportBaseRepository()
        repository.bind_types({
            Timestamp: TransportTimestampType,
            str: TransportStrType,
            int: TransportIntType,
            bool: TransportBoolType,
        })

        for value_type, transport_type in repository.direct_types_map.items():
            ## test consistency for binding and query of all defined transport types
            assert_that(repository.get_transport_type(value_type)).is_equal_to(transport_type)

        ## test consistency of object transport type definitions
        for cls in implementation_classes(ApiObject):
            obj_type_1 = repository.get_transport_type(cls)
            assert_that(issubclass(obj_type_1, TransportObjectType)).is_true()
            assert_that(issubclass(obj_type_1.storage_class, cls)).is_true()
            obj_type_2 = repository.get_transport_type(cls)
            assert_that(obj_type_1).is_equal_to(obj_type_2)

        ## test transport type definition for a values type with str member
        seq_type_1: TransportValuesType = repository.get_transport_type(Sequence[str])  # type: ignore[assignment]
        assert_that(issubclass(seq_type_1, TransportValuesType)).is_true()
        ## ensure that the repository is returning the original values type
        seq_type_2: TransportValuesType = repository.get_transport_type(Sequence[str])  # type: ignore[assignment]
        assert_that(seq_type_1).is_equal_to(seq_type_2)
        ## ensure that the member transport type matches the provided sequence member type
        assert_that(seq_type_1.member_transport_type.storage_class).is_equal_to(str)


if __name__ == '__main__':
    run_tests(__file__)
