"""Unit tetsts for pyfx.dispatch.oanda data model"""

from aenum import StrEnum, IntEnum  # type: ignore[import-untyped]
from datetime import datetime
import numpy as np
import pandas as pd
from pytest import mark
from typing import Annotated, Mapping, TYPE_CHECKING
from assertpy import assert_that  # type: ignore[import-untyped]
from zope.password.password import SHA1PasswordManager
from pyfx.dispatch.oanda.transport.account_id import AccountId  # type: ignore[import-untyped]

from pyfx.dispatch.oanda.models.common_types import AccountUnits, PriceValue, LotsValue, TransactionId

from pyfx.dispatch.oanda.test import ModelTest, MockFactory, run_tests
from pyfx.dispatch.oanda.transport.transport_fields import TransportField
from pyfx.dispatch.oanda.transport.transport_base import TransportTimestampType
from pyfx.dispatch.oanda.transport.data import ApiObject

from pyfx.dispatch.oanda.transport.transport_base import TransportBoolType, TransportFieldInfo, TransportFloatStrType, TransportIntType, TransportStrType, TransportType, TransportSecretStrType


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
        field_dt: Annotated[pd.Timestamp, TransportField(..., alias="fieldDt")]
        field_np_double: Annotated[np.double, TransportField(..., alias="fieldNpDouble")]

        field_int: Annotated[int, TransportField(..., alias="fieldInt")]
        field_str: Annotated[str, TransportField(...)]
        field_str_list: Annotated[list[str], TransportField(...)]
        field_acct_units: Annotated[AccountUnits, TransportField(...)]
        field_price: Annotated[PriceValue, TransportField(...)]
        field_lots: Annotated[LotsValue, TransportField(...)]
        field_txn_id: Annotated[TransactionId, TransportField(...)]

        field_acct: Annotated[AccountId, TransportField(...)]

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

        ## test nullable timestamp
        time_nat = pd.NaT
        assert_that(TransportTimestampType.parse('0') is time_nat).is_true()
        assert_that(TransportTimestampType.unparse_py(time_nat)).is_equal_to('0')

    @mark.dependency()
    def test_fields_map(self):
        cls = self.__class__
        mock_cls = cls.FieldsObject
        json_fields = mock_cls.json_fields
        model_fields = mock_cls.model_fields
        json_names = mock_cls.json_field_names
        assert_that(len(model_fields)).is_not_zero()
        for name, info in model_fields.items():
            assert_that(name in json_names).is_true()
            alias = info.alias
            if alias:
                assert_that(alias in json_fields).is_true()
            else:
                assert_that(name in json_fields).is_true()
            assert_that(isinstance(info, TransportFieldInfo)).is_true()
            assert_that(info.defining_class).is_equal_to(mock_cls)
        assert_that('field_str_list' in model_fields).is_true()
        assert_that(model_fields['field_str_list'].transport_type.member_transport_type).is_equal_to(TransportStrType)  # type: ignore[attr-defined]

    @mark.dependency(depends_on=['test_fields_map'])
    def test_field_recoding(self):
        cls = self.__class__
        mock_cls = cls.FieldsObject
        mock = cls.gen_mock()
        for attr, fieldinfo in mock_cls.model_fields.items():
            val = getattr(mock, attr)
            transport_type: TransportType = fieldinfo.transport_type
            ## unparse an intermediate literal value for transport encoding
            unparsed = transport_type.unparse_py(val, None)  # type: ignore[arg-type]
            assert_that(isinstance(unparsed, transport_type.serialization_class)).is_true()
            ## reparse as a storage value
            reparsed = transport_type.parse(unparsed)
            assert_that(isinstance(reparsed, transport_type.storage_class)).is_true()
            ## test for equivalence of the original and reparsed values
            assert_that(reparsed).is_equal_to(val)

    def test_encoding(self):
        cls = self.__class__
        mock = cls.gen_mock()

        ## test hashable support for account ID
        acct_id: AccountId = mock.field_acct
        assert_that(len(acct_id.get_secret_value())).is_not_equal_to(0)
        table = dict()
        table[acct_id] = hash(acct_id)
        assert_that(table[acct_id]).is_equal_to(hash(acct_id))

        ## test shadow support for account ID
        encoder = SHA1PasswordManager()
        ## first, ensure a consistent encoding in the IPasswordManager implementation
        ## - this should pass, when using the MD5 or SHA1 encoder
        ## - this may fail with BCRYPTPasswordManager and SMD5PasswordManager,
        ##   each of which may return a different value for the same string,
        ##   on each call to <...>.encodePassword()
        ## - other IPasswordManager implementations not yet tested
        mgr = SHA1PasswordManager()
        enc_first: bytes = mgr.encodePassword(acct_id.get_secret_value())
        enc_second: bytes = mgr.encodePassword(acct_id.get_secret_value())
        assert_that(enc_first).is_equal_to(enc_second)
        ## test encoding under <Credential>.get_shadow_value()
        shadowed = acct_id.get_shadow_value(encoder)
        assert_that(shadowed).is_equal_to(enc_first)
        ## test memoization
        shadowed_memoized = acct_id.get_shadow_value(encoder)
        assert_that(shadowed).is_equal_to(shadowed_memoized)

    def test_transport_display_string(self):
        cls = self.__class__
        mock_cls = cls.FieldsObject
        mock = cls.gen_mock()
        for attr, fieldinfo in mock_cls.model_fields.items():
            value = getattr(mock, attr)
            display = fieldinfo.transport_type.get_display_string(value)
            assert_that(isinstance(display, str)).is_true()


if __name__ == '__main__':

    run_tests(__file__)
    # from pprint import pformat
    # print("Mock: " + pformat(TestDataModel.gen_mock()))
