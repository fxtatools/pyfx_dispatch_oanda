
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.get_external_user_info200_response import GetExternalUserInfo200Response


class TestGetExternalUserInfo200Response(ModelTest):
    """GetExternalUserInfo200Response unit test stubs"""

    class Factory(MockFactory[GetExternalUserInfo200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
