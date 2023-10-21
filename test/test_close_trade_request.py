"""Unit test definition for TestCloseTradeRequest"""

from assertpy import assert_that

from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.close_trade_request import CloseTradeRequest, TransportDecmialAll
from pyfx.dispatch.oanda.models.common_types import DoubleConstants


class TestCloseTradeRequest(ModelTest):
    """CloseTradeRequest unit test stubs"""

    class Factory(MockFactory[CloseTradeRequest]):
        pass

    __factory__ = Factory

    def test_all_parse(self):
        parsed = TransportDecmialAll.parse("ALL")
        assert_that(parsed).is_equal_to(DoubleConstants.INF)

    def test_all_unparse(self):
        unparsed = TransportDecmialAll.unparse(DoubleConstants.INF)
        assert_that(unparsed).is_equal_to("ALL")

    def test_units_parse(self):
        parsed = TransportDecmialAll.parse("1.5")
        assert_that(parsed).is_equal_to(1.5)

    def test_units_unparse(self):
        unparsed = TransportDecmialAll.unparse(1.5)
        assert_that(unparsed).is_equal_to("1.5")


if __name__ == '__main__':
    run_tests(__file__)
