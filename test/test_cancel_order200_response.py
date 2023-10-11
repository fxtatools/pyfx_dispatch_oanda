"""Unit test definition for pyfx.dispatch.oanda"""

from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.cancel_order200_response import CancelOrder200Response

from assertpy import assert_that


class TestCancelOrder200Response(ModelTest):
    """CancelOrder200Response unit test stubs"""

    class Factory(MockFactory[CancelOrder200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
