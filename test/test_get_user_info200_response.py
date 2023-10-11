
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.get_user_info200_response import GetUserInfo200Response


class TestGetUserInfo200Response(ModelTest):
    """GetUserInfo200Response unit test stubs"""

    class Factory(MockFactory[GetUserInfo200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
