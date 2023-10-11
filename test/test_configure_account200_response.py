
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.configure_account200_response import ConfigureAccount200Response


class TestConfigureAccount200Response(ModelTest):
    """ConfigureAccount200Response unit test stubs"""

    class Factory(MockFactory[ConfigureAccount200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
