import numba as nb
from dataclasses import dataclass
from functools import partial
from numbers import Real
from typing_extensions import ClassVar
import numpy as np


from enum import Enum

from pyfx.dispatch.oanda.indicator.filter import SeriesFilter

import numpy.typing as npt
import pandas as pd


class SmoothedConst(float, Enum):
    PI = np.double(np.pi)
    PI_HALF = PI * 0.5
    PI_2 = PI * 2
    SQRT_2 = np.sqrt(2)
    SQRT_HALF = np.sqrt(0.5)


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