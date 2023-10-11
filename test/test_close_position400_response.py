
"""Unit test definition for pyfx.dispatch.oanda"""

from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.close_position400_response import ClosePosition400Response


class TestClosePosition400Response(ModelTest):
    """ClosePosition400Response unit test stubs"""

    class Factory(MockFactory[ClosePosition400Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
