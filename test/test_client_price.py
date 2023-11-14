"""Unit test definition for ClientPrice"""

from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.client_price import StreamingPrice


class TestClientPrice(ModelTest):
    """Unit test definition for ClientPrice"""

    class Factory(MockFactory[StreamingPrice]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
