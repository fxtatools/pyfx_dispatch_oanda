
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.list_open_positions200_response import ListOpenPositions200Response


class TestListOpenPositions200Response(ModelTest):
    """ListOpenPositions200Response unit test stubs"""

    class Factory(MockFactory[ListOpenPositions200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
