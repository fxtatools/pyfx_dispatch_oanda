"""Parser/Encoder Tests"""

from assertpy import assert_that  # type: ignore[import-untyped]
import os
import pandas as pd
from pprint import pprint
import pytest
from typing import TYPE_CHECKING
from typing_extensions import TypeVar

from pyfx.dispatch.oanda.test import PytestTest, run_tests

from pyfx.dispatch.oanda.util.paths import expand_path
from pyfx.dispatch.oanda.transport.data import ApiObject, JsonTypesRepository
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

from pyfx.dispatch.oanda.fx_const import FxLabel, FxCol

pytest_plugins = ('pytest_asyncio',)

SAMPLES_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__),  "sample_data"))

T_model = TypeVar("T_model", bound=ApiObject)


class TestParseUnparse(PytestTest):
    """Component Tests for parser and encoder frameworks"""

    async def run_builder_async(self, cls: type[T_model], samples_dir) -> T_model:
        """Parse a sample JSON file, returning an object of the file's model type"""
        JsonTypesRepository.__finalize_instance__()

        example_file = expand_path(cls.__name__ + ".json", samples_dir)
        if not os.path.exists(example_file):
            raise ValueError("No example file found", example_file)

        return await cls.afrom_file(example_file)

    def json_bytes(self, object: ApiObject):
        """return the bytes produced by an ApiObject's byte-wise JSON encoder"""
        return object.to_json_bytes()

    @pytest.fixture
    def samples_dir(self):
        return SAMPLES_DIR

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
    async def test_parse_unparse(self, model_cls, samples_dir):
        """Test parse, unparse, and value equivalence for models using sample JSON data"""

        # test that the parse completes
        rslt = await self.run_builder_async(model_cls, samples_dir)

        # test that the unparse completes
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
    async def test_candles_to_df(self, samples_dir):
        """Test dataframe output for GetInstrumentCandles200Response"""
        #
        # parse the sample response data
        #
        model_cls = GetInstrumentCandles200Response
        rslt: GetInstrumentCandles200Response = await self.run_builder_async(model_cls, samples_dir)
        #
        # create a dataframe from the sample response data
        #
        df: pd.DataFrame = rslt.to_df()

        if "TEST_PRINT_OBJECTS" in os.environ:
            print("Test %s => DataFrame" % model_cls.__name__)
            print(repr(df))

        assert_that(isinstance(df, pd.DataFrame)).is_true()

        if "TEST_PRINT_OBJECTS" in os.environ:
            df.info()
            print("Attributes:")
            pprint(df.attrs)

        candles = rslt.candles
        n_candles = len(candles)

        #
        # check the structure of the dataframe
        #
        df_shape = df.shape
        assert_that(len(df_shape)).is_equal_to(2)

        # check dtypes
        #
        # During development, the base dataframe schema
        # may be updated independent of the tests
        #
        # The set of unique dtype base types in the schema
        # should include least the following
        #
        #  - np.double : fx price values
        #  - np.uint32 : fx volume
        #
        dtt = tuple(df.dtypes)
        unique_dtypes = frozenset(dtt)
        assert_that(len(unique_dtypes)).is_greater_than_or_equal_to(2)
        dtchars = tuple(dt.char if hasattr(dt, "char") else None for dt in unique_dtypes)
        assert_that('d' in dtchars).is_true()  # fx price values
        assert_that('I' in dtchars).is_true()  # fx volume

        # check index structure
        idx = df.index
        assert_that(issubclass(idx.__class__, pd.DatetimeIndex)).is_true()
        for candle in candles:
            assert_that(candle.time in idx).is_true()

        # check for the expected number of dataframe rows
        assert_that(df_shape[0]).is_equal_to(n_candles)

        # check index label
        assert_that(df.index.name).is_equal_to(FxLabel.TIME)

        # check for multi-index columns, ensure contents per sample data
        cols = df.columns
        assert_that(isinstance(cols[0], tuple)).is_true()
        col_categories = frozenset(col[0] for col in cols)
        assert_that(len(col_categories)).is_greater_than_or_equal_to(3)
        assert_that(FxLabel.ASK in col_categories).is_true()
        assert_that(FxLabel.BID in col_categories).is_true()
        # the static sample data does not include fxtrade 'mid' quotes
        assert_that(FxLabel.MID not in col_categories).is_true()
        assert_that(FxLabel.VOLUME in col_categories).is_true()
        assert_that(FxLabel.COMPLETE in col_categories).is_true()

        l2_cols_uniq = frozenset(col[1] for col in cols)
        #
        # column labels in this section of the test would
        # include  "o", "h", "l", "c", and an empty string
        # for both the top-level "volume" and "complete"
        # columns e.g ("volume", "")
        #
        assert_that(len(l2_cols_uniq)).is_greater_than_or_equal_to(5)
        assert_that(FxLabel.OPEN in l2_cols_uniq).is_true()
        assert_that(FxLabel.HIGH in l2_cols_uniq).is_true()
        assert_that(FxLabel.LOW in l2_cols_uniq).is_true()
        assert_that(FxLabel.CLOSE in l2_cols_uniq).is_true()
        assert_that("" in l2_cols_uniq).is_true()

        # test dataframe annotations
        attrs = df.attrs
        assert_that("instrument" in attrs).is_true()
        assert_that(attrs['instrument']).is_equal_to(rslt.instrument.name)
        assert_that("granularity" in attrs).is_true()
        assert_that(attrs["granularity"]).is_equal_to(rslt.granularity)


if __name__ == "__main__":
    os.environ["TEST_PRINT_OBJECTS"] = "Defined"
    run_tests(__file__)
