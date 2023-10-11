## Unit tests for Transport Types Repository

from assertpy import assert_that
from pytest import mark

from collections.abc import Sequence
from pandas import Timestamp

from pyfx.dispatch.oanda.test import ComponentTest, run_tests
from pyfx.dispatch.oanda.transport.data import ApiObject
from pyfx.dispatch.oanda.transport.repository import TransportObject, TransportTypesRepository
from pyfx.dispatch.oanda.transport.transport_base import TransportValues
from pyfx.dispatch.oanda.transport.transport_types import TransportBool, TransportTimestamp, TransportStr, TransportInt


class TestDataModel(ComponentTest):
    """Unit tests for Transport Types Repository"""

    @mark.dependency()
    def test_a(self):
        pass

    @mark.dependency(depends_on=['test_a'])
    def test_transport_type_get(self):
        repository = TransportTypesRepository()
        repository.bind_map({
            Timestamp: TransportTimestamp,
            str: TransportStr,
            int: TransportInt,
            bool: TransportBool,
        })

        for value_type, transport_type in repository.direct_types_map.items():
            ## test handling for literal transport types
            assert_that(repository.get_transport_type(value_type)).is_equal_to(transport_type)

        ## test transport type definition (ApiObject)
        obj_type_1 = repository.get_transport_type(ApiObject)
        assert_that(issubclass(obj_type_1, TransportObject)).is_true()
        obj_type_2 = repository.get_transport_type(ApiObject)
        assert_that(obj_type_2.__name__).is_equal_to(obj_type_1.__name__)

        ## test transport type definitions - values type with str member
        seq_type_1 = repository.get_transport_type(Sequence[str])
        assert_that(issubclass(seq_type_1, TransportValues)).is_true()
        seq_type_2 = repository.get_transport_type(Sequence[str])
        assert_that(id(seq_type_2)).is_equal_to(id(seq_type_1))
        assert_that(seq_type_1.member_transport_type.storage_class).is_equal_to(str)

        ## test transport type definitions - values type with ApiObject member
        seq_type_3 = repository.get_transport_type(Sequence[ApiObject])
        assert_that(seq_type_3.member_transport_type.storage_class).is_equal_to(ApiObject)


if __name__ == '__main__':
    run_tests(__file__)
