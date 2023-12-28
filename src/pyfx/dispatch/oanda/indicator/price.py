"""Price Filter"""

from dataclasses import dataclass
from enum import IntEnum
from functools import partial

import numpy as np
import pandas as pd
import warnings

from typing import Callable
from typing_extensions import ClassVar

from pyfx.dispatch.oanda.fx_const import FxLabel
from pyfx.dispatch.oanda.indicator.common import ColumnName
from pyfx.dispatch.oanda.indicator.filter import Filter


class PriceSummary(IntEnum):
    OPEN = 1
    HIGH = 3
    LOW = 5
    CLOSE = 7
    MEDIAN = 1 << 8  # HL mean
    TYPICAL = 2 << 8  # HLC mean
    WEIGHTED = 3 << 8  # HLCC mean

    def direct(self):
        return self & 1


@dataclass(frozen=True)  # similar should be used in superclasses && subclasses
class PriceFilter(Filter[pd.DataFrame, pd.Series]):
    ##
    ## a working prototype for the data layer of an indicator system
    ##

    type_label: ClassVar[str] = "Price"

    label: str = type_label
    mode: PriceSummary = PriceSummary.TYPICAL

    # title: str = "Price"

    ## defaults per Candlestick object fields [OANDA fxTrade v20 API]
    c_open: ColumnName = FxLabel.OPEN.value
    c_high: ColumnName = FxLabel.HIGH.value
    c_low: ColumnName = FxLabel.LOW.value
    c_close: ColumnName = FxLabel.CLOSE.value

    def apply(self, df: pd.DataFrame) -> pd.Series:
        return self.price_func(df)(df)

    def price_func(self, df: pd.DataFrame) -> Callable[[pd.DataFrame], pd.Series]:

        if self.mode.direct():
            #
            # direct price modes
            #
            def cb(label, col, data: pd.DataFrame):
                means = pd.Series(data.loc[:, col], name=label, copy=False)
                means.attrs = data.attrs
                return means

            if self.mode is PriceSummary.OPEN:
                col = self.c_open
            elif self.mode is PriceSummary.HIGH:
                col = self.c_high
            elif self.mode is PriceSummary.LOW:
                col = self.c_low
            elif self.mode is PriceSummary.CLOSE:
                col = self.c_close

            return partial(cb, self.label, col)

        #
        # common inidirect price modes
        #
        elif self.mode is PriceSummary.MEDIAN:

            def cb(label, highcol, lowcol, table: pd.DataFrame,):
                #
                # numpy.mean() appears to use a mean() implementation
                # from pandas, when provided with a dataframe value.
                # The return value is consistently a pd.Series object
                #
                means: pd.Series = np.mean(table.loc[:, [highcol, lowcol]], axis=1)
                means.name = label
                return means

            return partial(cb, self.label, self.c_high, self.c_low)

        elif self.mode is PriceSummary.TYPICAL:

            def cb(label, highcol, lowcol, closecol, table: pd.DataFrame,):
                means: pd.Series = np.mean(table.loc[:, [highcol, lowcol, closecol]], axis=1)
                means.name = label
                return means

            return partial(cb, self.label, self.c_high, self.c_low, self.c_close)

        elif self.mode is PriceSummary.WEIGHTED:

            def cb(label, highcol, lowcol, closecol, table: pd.DataFrame):
                if table.flags.allows_duplicate_labels is True:
                    means: pd.Series = np.mean(table.loc[:, [highcol, lowcol, closecol, closecol]], axis=1)
                else:
                    high = table.loc[:, highcol].to_numpy(copy=False)
                    low = table.loc[:, lowcol].to_numpy(copy=False)
                    close = table.loc[:, closecol].to_numpy(copy=False)
                    # create an intermediate dataframe having unique column names
                    inter = pd.DataFrame(dict(h=high, l=low, c1=close, c2=close), index=table.index, copy=False)
                    inter.attrs = table.attrs
                    means = np.mean(inter, axis=1)
                means.name = label
                return means

            return partial(cb, self.label, self.c_high, self.c_low, self.c_close)
        #
        # undefined price mode
        #
        else:
            warnings.warn("Unknown price mode %r for %r" % (self.mode, self,),
                          stacklevel=3)

            def cb(table: pd.DataFrame):
                return np.empty(len(table.index)) * np.nan
            return cb

