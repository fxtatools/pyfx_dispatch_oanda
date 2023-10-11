
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.replace_order201_response import ReplaceOrder201Response


class TestReplaceOrder201Response(ModelTest):
    """ReplaceOrder201Response unit test stubs"""

    class Factory(MockFactory[ReplaceOrder201Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
