
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.list_positions200_response import ListPositions200Response


class TestListPositions200Response(ModelTest):
    """ListPositions200Response unit test stubs"""

    class Factory(MockFactory[ListPositions200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
