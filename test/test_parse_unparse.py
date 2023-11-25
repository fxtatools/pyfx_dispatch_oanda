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

    @pytest.mark.asyncio
    @pytest.mark.dependency(depends_on="test_parse_unparse")
    async def test_candles_to_df(self, examples_dir):
        """Test dataframe output for GetInstrumentCandles200Response"""
        model_cls = GetInstrumentCandles200Response
        rslt: GetInstrumentCandles200Response = await self.run_builder_async(model_cls, examples_dir)
        df = rslt.to_df()
        if "TEST_PRINT_OBJECTS" in os.environ:
            print("Test %s => DataFrame" % model_cls.__name__)
            print(repr(df))
        assert_that(isinstance(df, pd.DataFrame)).is_true()
        if TYPE_CHECKING:
            df: pd.DataFrame  # type: ignore[no-redef]
        if "TEST_PRINT_OBJECTS" in os.environ:
            df.info()
            print("Attributes:")
            pprint(df.attrs)
        candles = rslt.candles
        n_candles = len(candles)
        #
        # check structure of the dataframe
        #
        df_shape = df.shape
        assert_that(len(df_shape)).is_equal_to(2)
        # check dtypes
        dtt = tuple(df.dtypes)
        dtset = frozenset(dtt)
        assert_that(len(dtset)).is_equal_to(2)
        dtchars = tuple(dt.char for dt in dtset)
        assert_that('d' in dtchars).is_true()  # price values
        assert_that('l' in dtchars).is_true()  # volume
        # check index
        idx = df.index
        assert_that(issubclass(idx.__class__, pd.DatetimeIndex)).is_true()
        for candle in candles:
            assert_that(candle.time in idx).is_true()
        ## check for the expected number of dataframe rows
        assert_that(df_shape[0]).is_equal_to(n_candles)
        ## check for multi-index columns, ensure contents per input
        cols = df.columns
        assert_that(isinstance(cols[0], tuple)).is_true()
        col_categories = {col[0] for col in cols}
        assert_that(len(col_categories)).is_equal_to(3)
        assert_that("ask").is_in(*col_categories)
        assert_that("bid").is_in(*col_categories)
        assert_that("volume").is_in(*col_categories)
        assert_that("mid").is_not_in(*col_categories)
        col_quotes_uniq = {col[1] for col in cols}
        assert_that(len(col_quotes_uniq)).is_equal_to(5)
        assert_that("o").is_in(*col_quotes_uniq)
        assert_that("h").is_in(*col_quotes_uniq)
        assert_that("l").is_in(*col_quotes_uniq)
        assert_that("c").is_in(*col_quotes_uniq)
        assert_that("volume").is_in(*col_quotes_uniq)
        ## test dataframe annotations
        attrs = df.attrs
        assert_that("instrument" in attrs).is_true()
        assert_that(attrs['instrument']).is_equal_to(rslt.instrument.name)


if __name__ == "__main__":
    os.environ["TEST_PRINT_OBJECTS"] = "Defined"
    run_tests(__file__)
