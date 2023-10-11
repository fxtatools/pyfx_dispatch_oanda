
"""Unit test definition for pyfx.dispatch.oanda"""

from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.close_position404_response import ClosePosition404Response


class TestClosePosition404Response(ModelTest):
    """ClosePosition404Response unit test stubs"""

    class Factory(MockFactory[ClosePosition404Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
