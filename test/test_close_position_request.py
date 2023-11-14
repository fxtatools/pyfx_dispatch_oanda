"""Unit test definition for ClosePositionRequest"""

from assertpy import assert_that  # type: ignore[import-untyped]

from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.close_position_request import ClosePositionRequest, TransportDecimalAllNone
from pyfx.dispatch.oanda.models.common_types import DoubleConstants


class TestClosePositionRequest(ModelTest):
    """ClosePositionRequest unit test stubs"""

    class Factory(MockFactory[ClosePositionRequest]):
        pass

    __factory__ = Factory

    def test_all_parse(self):
        parsed = TransportDecimalAllNone.parse("ALL")
        assert_that(parsed).is_equal_to(DoubleConstants.INF)

    def test_all_unparse(self):
        unparsed = TransportDecimalAllNone.unparse_py(DoubleConstants.INF)
        assert_that(unparsed).is_equal_to("ALL")

    def test_none_parse(self):
        parsed = TransportDecimalAllNone.parse("NONE")
        assert_that(parsed).is_equal_to(DoubleConstants.ZERO)

    def test_none_unparse(self):
        unparsed = TransportDecimalAllNone.unparse_py(DoubleConstants.ZERO)
        assert_that(unparsed).is_equal_to("NONE")

    def test_units_parse(self):
        parsed = TransportDecimalAllNone.parse("1.5")
        assert_that(parsed).is_equal_to(1.5)

    def test_units_unparse(self):
        unparsed = TransportDecimalAllNone.unparse_py(1.5)
        assert_that(unparsed).is_equal_to("1.5")


if __name__ == '__main__':
    run_tests(__file__)
