"""Parser/Encoder Tests"""

import asyncio as aio
from contextlib import closing
import concurrent.futures as cofutures
import ijson  # type: ignore[import-untyped]
import os
import pytest
from typing import Union

from pyfx.dispatch.oanda.test import PytestTest, run_tests

from pyfx.dispatch.oanda.util.paths import expand_path, Pathname
from pyfx.dispatch.oanda.transport.data import ApiObject, ApiClass, JsonTypesRepository
from pyfx.dispatch.oanda.io import AsyncSegmentChannel
from pyfx.dispatch.oanda.parser import ModelBuilder
from pyfx.dispatch.oanda.models import (
    ListAccounts200Response,
    GetAccount200Response,
    GetAccountSummary200Response,
    GetAccountInstruments200Response,
    GetInstrumentCandles200Response,
    GetTransactionRange200Response,
    ListOrders200Response,
    ListTrades200Response
)

pytest_plugins = ('pytest_asyncio',)

EXAMPLES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),  "json_samples"))

T_model = TypeVar("T_model", bound=ApiObject)


class TestParseUnparse(PytestTest):
    """Component Tests for parser and encoder frameworks"""

    async def run_builder_async(self, cls: type[T_model], examples_dir) -> T_model:
        """Parse a sample JSON file, returning an object of the file's model type"""
        JsonTypesRepository.__finalize_instance__()

        example_file = expand_path(cls.__name__ + ".json", examples_dir)
        if not os.path.exists(example_file):
            raise ValueError("No example file found", example_file)

        return await cls.afrom_file(example_file)

    def json_bytes(self, object: ApiObject):
        """return the bytes produced by an ApiObject's byte-wise JSON encoder"""
        return object.to_json_bytes()

    @pytest.fixture
    def examples_dir(self):
        return EXAMPLES_DIR

    @pytest.mark.asyncio
    @pytest.mark.dependency()
    @pytest.mark.parametrize(
        "model_cls", [
            ListAccounts200Response,
            GetAccount200Response,
            GetAccountSummary200Response,
            GetAccountInstruments200Response,
            GetInstrumentCandles200Response,
            GetTransactionRange200Response,
            ListOrders200Response,
            ListTrades200Response
        ]
    )
    async def test_parse_unparse(self, model_cls, examples_dir):
        """Test parse, unparse, and value equivalence for models, using sample JSON data"""
        ## test parse
        rslt = await self.run_builder_async(model_cls, examples_dir)
        ## test unparse
        b = self.json_bytes(rslt)

        print_results = "TEST_PRINT_OBJECTS" in os.environ
        if print_results:
            ## print the results for visual inspection
            ## - parsed repr
            ## - bytes repr
            print()
            print("unparsed %s object" % rslt.__class__.__name__)
            print("  " + repr(rslt))
            print()
            print("=> " + repr(b))


if __name__ == "__main__":
    os.environ["TEST_PRINT_OBJECTS"] = "Defined"
    run_tests(__file__)
