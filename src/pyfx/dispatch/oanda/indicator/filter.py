# indicator-as-data-filter framework - prototypes
#
#
# architecture (notes):
# - I/O channel [fxpy]
# - data processing [indicator.py]
# - filter UI [indicator_ui.py]
#
# prototypes for the data processing and filter UI components
#

from abc import ABC, abstractmethod
from functools import partial

from dataclasses import dataclass, field

from numbers import Real

import numba as nb
import numpy as np
import numpy.typing as npt
import pandas as pd

import warnings

from enum import Enum, IntEnum

from typing import Callable, Generic, Optional, Sequence, Union
from typing_extensions import ClassVar, Self, TypeAlias, TypeVar


from pyfx.dispatch.oanda.fx_const import FxLabel, FxCol


class IndicatorManager():
    pass


class LabelMixin:
    pass


T_in = TypeVar("T_in", bound="Filter")


class IndicatorProvider(LabelMixin, Generic[T_in], ABC):
    ## TBD @ plugins, registration, indexing, and mostly: UI
    @abstractmethod
    def initialize_indicator(self, *args, **kwargs) -> T_in:
        pass


class PandasData(pd.core.generic.NDFrame, pd.core.arraylike.OpsMixin, ABC):
    # initial prototype
    #
    # TBD:
    # - Filters onto pandas series
    # - Filters onto numpy ndarrays
    #
    # In the working prototypes, data processing is managed
    # generally onto pandas.DataFrame objects.
    #
    # Each filter definition may produce any small number of
    # numpy.ndarray objects internaly, ideally with non-copying
    # calls onto the input dataframe columns. These ndarray
    # objects are then generally discarded after translation
    # to an output dataframe.
    #
    # Hypothetically, the ndarray references may be retained
    # at some instance scope, for processing within the Filter UI
    pass


T_data = TypeVar("T_data", bound=PandasData)  # nondirectional bound
T_i = TypeVar("T_i", bound=PandasData)  # dataframe-like input
T_o = TypeVar("T_o", bound=PandasData)  # dataframe-like output


@dataclass(frozen=True)
class Filter(LabelMixin, Generic[T_i, T_o], ABC):

    @abstractmethod
    def apply(self, df: T_i) -> T_o:
        pass


class PriceSummary(IntEnum):
    OPEN = 1
    HIGH = 3
    LOW = 5
    CLOSE = 7
    MEDIAN = 1 << 8  # HL mean
    TYPICAL = 2 << 8  # HLC mean
    WEIGHTED = 3 << 8  # HLCC mean
    SMOOTHED = 0xFE  # Uncommon price summary method

    def direct(self):
        return self & 1


#
# Localized column name type
#
# - in application, not mixing int and str column labels
#
# - there may be other approaches available for unique
#   column names, not addressed in the following
#
ColumnName: TypeAlias = Union[str, tuple[str, ...]]


#
# the following represents an initial approach for dataframe schema definitions
#

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


class SmoothedConst(float, Enum):
    PI = np.double(np.pi)
    PI_HALF = PI * 0.5
    PI_2 = PI * 2
    SQRT_2 = np.sqrt(2)
    SQRT_HALF = np.sqrt(0.5)


class WindowFilter(Filter[T_i, T_o]):
    window_size: ClassVar[int] = -1
    min_periods: ClassVar[int] = -1


class SeriesFilter(WindowFilter[pd.Series, pd.Series]):
    pass


# assuming other indicator classes are defined as frozen (FIXME)

@dataclass(frozen=True)
class Smoothed(SeriesFilter):

    """Python Adaptation of the Super Smoother filter by John F. Ehlers

    Reference:

    Ehlers, John F. (2013). The Hilbert Transformer. In Cycle Analytics for Traders:
        Advanced Technical Trading Concepts (pp. 175–194). Wiley
    """

    window_size: ClassVar[np.int8] = nb.uchar(2)
    min_periods: ClassVar[np.int8] = nb.uchar(0)

    type_label: ClassVar[str] = "Smoothed"
    label: str = type_label

    #
    # user-configurable
    #
    # 20 is the default period in the original example
    #
    # for period values less than 4 the indicator may be notably
    # less smoothed, though also less generally lagged
    #
    # floating-point values may in fact be used here
    #
    ##
    period: Real = 4

    #
    # application data
    #
    c2: float = np.NAN
    c3: float = np.NAN
    c1: float = np.NAN

    def set_factors(self, period: int):
        #
        # set calculation factors for the indicator
        #

        # setattr func for constant factors,
        #
        # this works around the dataclass 'frozen' catch
        #
        set = partial(object.__setattr__, self)

        # set the indicator period, catching integer overflow
        #
        # the period value for this indicator is used mainly for
        # calculating the indicator constants. The value will be
        # stored with a floating-point type
        #
        p = np.double(period)
        if p == 0:
            p = np.longdouble(period)
        if p == 0:
            raise ValueError("period value is too large for numpy.longdouble type", period)
        set("period", p)

        # constant factors
        #
        # the following factors are constant within the instance scope,
        # assuming a constant indicator period
        #
        a1 = np.exp(-SmoothedConst.SQRT_2 * SmoothedConst.PI / p)
        b1 = np.double(2) * a1 * np.cos(SmoothedConst.SQRT_2 * SmoothedConst.PI_HALF / p)
        c2 = b1
        c3 = -(a1 * a1)
        c1 = np.double(1) - c2 - c3
        set("c1", c1)
        set("c2", c2)
        set("c3", c3)

    def __init__(self, *, period: int = period, label: str = "sprice"):
        set = partial(object.__setattr__, self)
        # set instance metadata
        set("label", label)
        self.set_factors(period)

    def apply(self, ser: pd.Series) -> pd.Series:
        c1: np.double = self.c1
        c2: np.double = self.c2
        c3: np.double = self.c3

        #
        # initialize the intermediate values buffer
        #
        prebuf: npt.NDArray[np.double] = np.empty(2, dtype=np.double)
        pre_0 = ser.iloc[0]
        pre_1 = ser.iloc[0:1].mean()
        prebuf[0] = pre_0
        prebuf[1] = pre_1

        @nb.jit(nopython=True, nogil=True)
        def calc(vals: nb.float64[:, :],
                 c1: nb.float64, c2: nb.float64, c3: nb.float64,
                 prebuf: nb.float64[:]) -> nb.double:
            #
            # primary Super Smoother calculation
            #
            pre_0 = prebuf[0]
            pre_1 = prebuf[1]
            m = vals.mean()
            smoothed = (c1 * m) + (c2 * pre_1) + (c3 * pre_0)
            prebuf[1] = smoothed
            prebuf[0] = pre_1
            return smoothed

        nbargs = dict(nopython=True, nogil=True)
        s: pd.Series = ser.rolling(self.window_size, self.min_periods).apply(
            calc, engine="numba", engine_kwargs=nbargs, raw=True,
            args=(c1, c2, c3, prebuf,)
        )
        s.name = self.label
        s.attrs = ser.attrs
        return s
