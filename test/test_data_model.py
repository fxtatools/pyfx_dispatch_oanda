"""Unit tetsts for pyfx.dispatch.oanda data model"""

from aenum import StrEnum, IntEnum
from datetime import datetime
import numpy as np
import pandas as pd
from pytest import mark
from typing import Annotated, Mapping
from assertpy import assert_that


from pyfx.dispatch.oanda.models.common_types import AccountUnits, PriceValue, LotsValue

from pyfx.dispatch.oanda.test import ModelTest, MockFactory, run_tests
from pyfx.dispatch.oanda.transport.transport_fields import TransportField
from pyfx.dispatch.oanda.transport.transport_base import TransportTimestampType
from pyfx.dispatch.oanda.transport.data import ApiObject

from pyfx.dispatch.oanda.transport.repository import TransportBaseRepository

from pyfx.dispatch.oanda.transport.transport_base import TransportBoolType, TransportFieldInfo, TransportFloatStrType, TransportIntType, TransportStrType, TransportType


class TestDataModel(ModelTest):
    """Unit tetsts for pyfx.dispatch.oanda data model"""

    class TestStrEnum(StrEnum):
        test_a = "test_a",
        test_b = "test_b"

    class TestIntEnum(IntEnum):
        test_0 = 0
        test_1 = 1

    class FieldsObject(ApiObject):
        # base class for model mock tests, using polyfactory
        field_dt: Annotated[pd.Timestamp,TransportField(..., alias="fieldDt")]
        field_np_double: Annotated[np.double,TransportField(..., alias="fieldNpDouble")]

        field_int: Annotated[int,TransportField(..., alias="fieldInt")]
        field_str: Annotated[str, TransportField(...)]
        field_str_list: Annotated[list[str],TransportField(...)]
        field_acct_units: Annotated[AccountUnits, TransportField(...)]
        field_price: Annotated[PriceValue, TransportField(...)]
        field_lots: Annotated[LotsValue, TransportField(...)]

    class Factory(MockFactory[FieldsObject]):
        pass

    __factory__ = Factory


    def test_literal_types(self):
        specs: Mapping[type[TransportType], tuple[type, type]] = {
            TransportBoolType: (bool, bool,),
            TransportStrType: (str, str,),
            TransportFloatStrType: (np.double, str,),
            TransportIntType: (int, int,),
            TransportTimestampType: (datetime, str,),
        }
        for t_type, (icls, ocls) in specs.items():
            assert_that(t_type.storage_class).is_equal_to(icls)
            assert_that(t_type.serialization_class).is_equal_to(ocls)

    @mark.dependency()
    def test_fields_map(self):
        cls = self.__class__
        mock_cls = cls.FieldsObject
        json_fields = mock_cls.json_fields
        model_fields = mock_cls.model_fields
        json_names = mock_cls.json_field_names
        assert_that(len(model_fields)).is_not_zero()
        for name, fieldinfo in model_fields.items():
            assert_that(name in json_names).is_true()
            alias = fieldinfo.alias
            if alias:
                assert_that(alias in json_fields).is_true()
            else:
                assert_that(name in json_fields).is_true()
            assert_that(isinstance(fieldinfo, TransportFieldInfo)).is_true()
            assert_that(fieldinfo.defining_class).is_equal_to(mock_cls)
        assert_that('field_str_list' in model_fields).is_true()
        assert_that(model_fields['field_str_list'].transport_type.member_transport_type).is_equal_to(TransportStrType)

    @mark.dependency(depends_on=['test_fields_map'])
    def test_field_recoding(self):
        cls = self.__class__
        mock_cls = cls.FieldsObject
        mock = cls.gen_mock()
        for attr, fieldinfo in mock_cls.model_fields.items():
            val = getattr(mock, attr)
            transport_type: type[TransportType] = fieldinfo.transport_type
            ## unparse as an intermediate value for transport encoding, generally a string
            unparsed = transport_type.unparse_py(val, None)
            assert_that(isinstance(unparsed, transport_type.serialization_class)).is_true()
            ## reparse as a Python value
            reparsed = transport_type.parse(unparsed)
            assert_that(isinstance(reparsed, transport_type.storage_class)).is_true()
            ## test for equivalence of the original and reparsed values
            assert_that(reparsed).is_equal_to(val)


if __name__ == '__main__':
    run_tests(__file__)
    # from pprint import pformat
    # print("Mock: " + pformat(TestDataModel.gen_mock()))
