## unit tests for pyfx.dispatch.oanda.data

from aenum import Enum, StrEnum, IntEnum
import asyncio as aio
import numpy as np
import pandas as pd
from pydantic import Field, field_serializer
from pytest import mark
from typing import Mapping
from assertpy import assert_that


from polyfactory.factories.attrs_factory import AttrsFactory
from pyfx.dispatch.oanda.models.common_types import AccountUnits

from pyfx.dispatch.oanda.test import ComponentTest, ModelTest, MockFactory, run_tests
from pyfx.dispatch.oanda.transport.transport_fields import TransportField
from pyfx.dispatch.oanda.transport.transport_types import TransportBool, TransportTimestamp, TransportFloatStr, TransportInt, TransportStr
from pyfx.dispatch.oanda.transport.data import ApiObject

from pyfx.dispatch.oanda.transport.repository import TransportTypesRepository

from pyfx.dispatch.oanda.transport.transport_base import TransportFieldInfo, TransportType, TransportValues


class TestDataModel(ModelTest):
    """Unit tests for pyfx.dispatch.oanda.data"""

    class TestStrEnum(StrEnum):
        test_a = "test_a",
        test_b = "test_b"

    class TestIntEnum(IntEnum):
        test_0 = 0
        test_1 = 1

    class FieldsObject(ApiObject):
        field_dt: pd.Timestamp = TransportField(..., alias="fieldDt")
        field_np_double: np.double = TransportField(..., alias="fieldNpDouble")

        field_int: int = TransportField(..., alias="fieldInt")
        field_str: str = TransportField(...)
        field_str_list: list[str] = TransportField(...)
        fields_acct_units: AccountUnits = TransportField(...)

    class Factory(MockFactory[FieldsObject]):
        pass

    __factory__ = Factory

    @field_serializer("thunk", when_used="always")
    def thunk(self):
        pass

    def test_literal_types(self):
        specs: Mapping[type[TransportType], tuple[type]] = {
            TransportBool: (bool, str,),
            TransportStr: (str, str,),
            # TransportFloatStr: (float, str,),
            TransportFloatStr: (np.float64, str,),
            TransportInt: (int, int,),
            TransportTimestamp: (pd.Timestamp, str,),
        }
        for t_type, (icls, ocls) in specs.items():
            assert_that(t_type.storage_class).is_equal_to(icls)
            assert_that(t_type.serialization_class).is_equal_to(ocls)

    @mark.dependency()
    def test_fields_map(self):
        cls = self.__class__
        mock_cls = cls.FieldsObject
        field_map = mock_cls.api_fields
        model_fields = mock_cls.model_fields
        json_names = mock_cls.json_field_names
        assert_that(len(model_fields)).is_not_zero()
        for name, fieldinfo in model_fields.items():
            assert_that(name in field_map).is_true()
            assert_that(name in json_names).is_true()
            alias = fieldinfo.alias
            if alias:
                assert_that(alias in field_map).is_true()
            assert_that(isinstance(fieldinfo, TransportFieldInfo)).is_true()
            fieldinfo: TransportFieldInfo
            assert_that(fieldinfo.defining_class).is_equal_to(mock_cls)
        assert_that('field_str_list' in model_fields).is_true()
        assert_that(model_fields['field_str_list'].transport_type.member_transport_type).is_equal_to(TransportStr)

    @mark.dependency(depends_on=['test_fields_map'])
    def test_field_recoding(self):
        cls = self.__class__
        mock_cls = cls.FieldsObject
        mock = cls.gen_mock()
        for attr, fieldinfo in mock_cls.model_fields.items():
            val = getattr(mock, attr)
            transport_type: type[TransportType] = fieldinfo.transport_type
            ## unparse as an intermediate value for transport encoding, generally a string
            unparsed = transport_type.unparse(val, None)
            assert_that(isinstance(unparsed, transport_type.serialization_class)).is_true()
            ## reparse as a Python value
            reparsed = transport_type.parse(unparsed)
            assert_that(isinstance(reparsed, transport_type.storage_class)).is_true()
            ## test for equivalence of the original and reparsed values
            assert_that(reparsed).is_equal_to(val)


    def test_field_inference(self):
        thunk = TransportTypesRepository()
        pass


if __name__ == '__main__':
    run_tests(__file__)
    # from pprint import pformat
    # print("Mock: " + pformat(TestDataModel.gen_mock()))
