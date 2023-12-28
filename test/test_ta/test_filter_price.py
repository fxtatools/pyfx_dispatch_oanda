"""Unit tests for PriceFilter and the PriceSummary enum"""

from assertpy import assert_that
import numpy as np
import os
import pandas as pd
import pytest
from typing import Optional
from pyfx.dispatch.oanda.test import ComponentTest, run_tests

from pyfx.dispatch.oanda.util.ndata import dataframe_from_npz
from pyfx.dispatch.oanda.fx_const import FxLabel

#
# the components to test
#
from pyfx.dispatch.oanda.indicator.price import PriceFilter, PriceSummary


EXAMPLES_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sample_data"))

ASK: Optional[pd.DataFrame] = None


@pytest.fixture
def ask() -> pd.DataFrame:
    global ASK
    if ASK is None:
        ASK = dataframe_from_npz(os.path.join(EXAMPLES_DIR, "quotes.npz")).loc[:, "ask"]
    return ASK


class TestPriceFiler(ComponentTest):

    def run_price(self, filter: PriceFilter, data: pd.DataFrame) -> pd.Series:
        # common price series tests
        prices: pd.Series = filter.apply(data)
        assert_that(prices.shape).is_equal_to(data.index.shape)
        assert_that(isinstance(prices, pd.Series)).is_true()
        assert_that((prices.index == data.index).all()).is_true()
        assert_that(prices.name).is_equal_to(filter.label)
        assert_that(prices.attrs).is_equal_to(data.attrs)
        return prices

    @pytest.mark.parametrize(
        "summary", [
            PriceSummary.OPEN,
            PriceSummary.HIGH,
            PriceSummary.LOW,
            PriceSummary.CLOSE,
        ])
    def test_price_summary_direct(self, summary: PriceSummary):
        #
        # ensure that each of these modes of price summary
        # *is denoted as* a direct mode of price summary
        #
        # the 'direct' flag will be used when selecting a
        # callback func in PriceSummary.apply()
        #
        assert_that(summary.direct()).is_true()

    @pytest.mark.parametrize(
        "summary", [
            PriceSummary.MEDIAN,
            PriceSummary.TYPICAL,
            PriceSummary.WEIGHTED
        ])
    def test_price_summary_indirect(self, summary: PriceSummary):
        #
        # ensure that each of these modes of price summary
        # *is not denoted as* a direct mode of price summary
        #
        assert_that(summary.direct()).is_false()

    @pytest.mark.parametrize(
        "summary", [
            PriceSummary.OPEN,
            PriceSummary.HIGH,
            PriceSummary.LOW,
            PriceSummary.CLOSE,
        ])
    def test_price_filter_direct(self, ask: pd.DataFrame, summary: PriceSummary):
        #
        # for each of the open, high, low and close modes of price summary onto
        # PriceFilter, ensure that the series returned by the price filter matches
        # the column of the corresponding price series
        #
        colname = FxLabel[summary.name].value  # e.g "o" given "OPEN"
        filter = PriceFilter(mode=summary)
        prices = self.run_price(filter, ask)
        col = ask.loc[:, colname]
        assert_that((prices == col).all()).is_true()
        assert_that(prices.attrs).is_equal_to(ask.attrs)

    def test_price_filter_median(self, ask: pd.DataFrame):
        #
        # test the median price filter
        #
        filter = PriceFilter(mode=PriceSummary.MEDIAN)
        prices = self.run_price(filter, ask)
        median = np.mean([ask.loc[:, FxLabel.HIGH], ask.loc[:, FxLabel.LOW]], axis=0)
        assert_that((prices == median).all()).is_true()
        assert_that(prices.attrs).is_equal_to(ask.attrs)

    def test_price_filter_typical(self, ask: pd.DataFrame):
        #
        # test the typiccal price filter
        #
        filter = PriceFilter(mode=PriceSummary.TYPICAL)
        prices = self.run_price(filter, ask)
        typical = np.mean([ask.loc[:, FxLabel.HIGH], ask.loc[:, FxLabel.LOW], ask.loc[:, FxLabel.CLOSE]], axis=0)
        assert_that((prices == typical).all()).is_true()
        assert_that(prices.attrs).is_equal_to(ask.attrs)

    def test_price_filter_weighted_dupok(self, ask: pd.DataFrame):
        #
        # test the weighted price filter with ask.allow_duplicate_labels=True
        #
        filter = PriceFilter(mode=PriceSummary.WEIGHTED)
        ask = ask.set_flags(allows_duplicate_labels=True, copy=False)
        prices = self.run_price(filter, ask)
        close = ask.loc[:, FxLabel.CLOSE]
        weighted = np.mean([ask.loc[:, FxLabel.HIGH], ask.loc[:, FxLabel.LOW], close, close], axis=0)
        assert_that((prices == weighted).all()).is_true()
        assert_that(prices.attrs).is_equal_to(ask.attrs)

    def test_price_filter_weighted_nodup(self, ask: pd.DataFrame):
        #
        # test the weighted price filter with ask.allow_duplicate_labels=False
        #
        filter = PriceFilter(mode=PriceSummary.WEIGHTED)
        ask = ask.set_flags(allows_duplicate_labels=False, copy=False)
        prices = self.run_price(filter, ask)
        close = ask.loc[:, FxLabel.CLOSE]
        weighted = np.mean([ask.loc[:, FxLabel.HIGH], ask.loc[:, FxLabel.LOW], close, close], axis=0)
        assert_that((prices == weighted).all()).is_true()
        assert_that(prices.attrs).is_equal_to(ask.attrs)


if __name__ == "__main__":
    run_tests(__file__)
