
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.cancel_order404_response import CancelOrder404Response


class TestCancelOrder404Response(ModelTest):
    """CancelOrder404Response unit test stubs"""

    class Factory(MockFactory[CancelOrder404Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
