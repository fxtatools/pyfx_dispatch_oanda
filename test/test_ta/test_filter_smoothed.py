"""Unit tests for the Super Smoother implementation in Python"""

from assertpy import assert_that

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
from pyfx.dispatch.oanda.indicator.filter import PriceFilter, PriceSummary, Smoothed


EXAMPLES_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sample_data"))

ASK: Optional[pd.DataFrame] = None


@pytest.fixture
def ask() -> pd.DataFrame:
    global ASK
    if ASK is None:
        ASK = dataframe_from_npz(os.path.join(EXAMPLES_DIR, "quotes.npz")).loc[:, "ask"]
    return ASK


@pytest.fixture
def pf():
    return PriceFilter(mode=PriceSummary.TYPICAL)


@pytest.fixture
def price(pf: PriceFilter, ask: pd.DataFrame) -> pd.Series:
    return pf.apply(ask)


class TestPriceFiler(ComponentTest):

    def test_smoothed(self, price: pd.Series, ask: pd.DataFrame):
        fil: Smoothed = Smoothed()
        smoothed: pd.Series = fil.apply(price)
        assert_that(smoothed.shape).is_equal_to(price.shape)
        assert_that((smoothed.index == ask.index).all()).is_true()
        assert_that(smoothed.name).is_equal_to(fil.label)
        assert_that(smoothed.attrs).is_equal_to(ask.attrs)

        # bounds test
        #
        # Needs review: Data points where smoothed > high or smoothed < low,
        # for smoothed = Smoothed().apply(typical_price or median_price)
        # and high, low, as series of the dataframe for price
        #
        # In short, these bounds tests would fail if using all()
        # in place of any()

        high = ask.loc[:, FxLabel.HIGH]
        assert_that((high >= smoothed).any()).is_true()

        low = ask.loc[:, FxLabel.LOW]
        assert_that((low <= smoothed).any()).is_true()

        # a more general bounds test
        assert_that(smoothed.max()).is_less_than_or_equal_to(price.max())
        assert_that(smoothed.min()).is_greater_than_or_equal_to(price.min())


if __name__ == "__main__":
    run_tests(__file__)
