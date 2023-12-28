"""Common definitions for indicators"""

from abc import ABC, abstractmethod
from datetime import datetime
from functools import partial
from itertools import chain
import numba
from numbers import Number
import numpy as np
import pandas as pd

from collections.abc import Sequence

from typing import Annotated, Optional, Union
from typing_extensions import get_args, get_type_hints, TypeAlias


from pyfx.dispatch.oanda.util.typeref import TypeRef


#
# Common Types
#


# generalized types for pandas column, index references
ColumnName: TypeAlias = Union[str, tuple[str, ...]]
ColumnRef: TypeAlias = Union[ColumnName, int]
RowRef: TypeAlias = Union[Number, datetime, pd.Period]


FreqData: TypeAlias = Union[pd.DataFrame, pd.Series, pd.TimedeltaIndex, pd.DatetimeIndex, pd.PeriodIndex]


class DataFrameLike(ABC):
    # abstract protocol class

    @property
    @abstractmethod
    def columns(self) -> Sequence[ColumnRef]:
        raise NotImplementedError(self.columns)

    @property
    @abstractmethod
    def index(self) -> Sequence[RowRef]:
        raise NotImplementedError(self.index)


class PandasData(pd.core.generic.NDFrame, pd.core.arraylike.OpsMixin, ABC):
    # abstract base class for Pandas DataFrame, Series structures
    pass


#
# metaprogramming util
#


def get_annotation(name: str, scope: type) -> Optional[TypeRef]:
    annot = get_type_hints(scope)
    scoped = annot.get(name, None)
    if isinstance(scoped, Annotated):
        return get_args(scoped)[0]
    else:
        return scoped


#
# data util
#

@numba.jit(nopython=True, nogil=True)
def usec(n: numba.uint64[:]) -> numba.uint64[:]:
    ## truncate an np times array as uint64 to uint64 seconds
    return n * 10**-9


def interpolate_freq(data: FreqData) -> Optional[pd.PeriodDtype]:
    # [prototype]
    #
    # infer a frequency for some dataframe or series with a time index,
    # or from a literal index
    #
    # returns a frequency string if a frequency could be inferred,
    # None if no frequency can be inferred by this approach
    #
    # this operates generally for a dataframe having a time index
    # with a number n >= 2 of index values continuous under a
    # pandas time index frequency. This will allow for discontinuous
    # values,  discarding the "None" case when some frequency can be
    # determined from other values in the index
    #
    # for a pd.DatetimeIndex, this will return the "Most frequently
    # occurring" frequency. Given a tie between two frequency values,
    # the first occurring, non-None frequency will be returned
    #
    # FIXME needs test under time delta index
    #
    ##
    if len(data) < 3:
        return None

    if isinstance(data, pd.PeriodIndex):
        return data.freq

    f = pd.infer_freq(data)
    if f is not None:
        # using the frequency inferred by pandas
        return pd.PeriodDtype(f)
    #
    # collect values form infer_freq() under rolling().apply()
    #
    idx = data.index if isinstance(data, (pd.DataFrame, pd.Series,)) else data
    freqs = {}
    icls = idx.__class__

    def parse(icls, dct, row):
        #
        # create a new index for each call within
        # rolling(3).apply(... parse ...), then
        # inferring  a frequency from the minimum
        # index. This uses the same index class
        # as used for the input value
        #
        # this will operate by side effect,
        # accumulating the number of occurrences
        # of distinct frequency strings in dct
        #
        # the return value from rolling().apply()
        # will be discarded, here
        #
        f = pd.infer_freq(icls(row))
        if f is not None:
            try:
                dct[f] += 1
            except KeyError:
                dct[f] = 1
        return np.nan
    intermediate = pd.DataFrame(dict(utime=idx.to_numpy(dtype=np.uint64)), index=idx)
    intermediate.rolling(3).apply(partial(parse, icls, freqs), raw=True)
    nfreq = len(freqs)
    if nfreq == 1:
        # simplest case: one predominant frequency, with any number > 0
        # of inconsistent values for which pd.infer_freq([a0, a1, a2]) => None
        freq = next(chain(freqs.keys()))
        return pd.PeriodDtype(freq)
    elif nfreq == 0:
        return None
    max = np.array(tuple(freqs.values()), dtype=int).max()
    # initial prototype: using the first most frequent frequency str
    #
    # with the previous checks, StopIteration should not be reached here
    #
    freq = next(k for k, v in freqs.items() if v == max)
    return pd.PeriodDtype(freq)
