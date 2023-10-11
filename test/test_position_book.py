
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.position_book import PositionBook


class TestPositionBook(ModelTest):
    """PositionBook unit test stubs"""

    class Factory(MockFactory[PositionBook]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
