# indicator-as-data-filter framework - prototypes

from abc import ABC, abstractmethod
from dataclasses import dataclass
import pandas as pd

from typing import Generic
from typing_extensions import ClassVar, TypeVar

from pyfx.dispatch.oanda.indicator.common import PandasData


class LabelMixin:
    pass


T_data = TypeVar("T_data", bound=PandasData)  # nondirectional bound
T_i = TypeVar("T_i", bound=PandasData)  # input data type
T_o = TypeVar("T_o", bound=PandasData)  # output data type


@dataclass(frozen=True)
class Filter(LabelMixin, Generic[T_i, T_o], ABC):

    @abstractmethod
    def apply(self, df: T_i) -> T_o:
        pass


class WindowFilter(Filter[T_i, T_o]):
    window_size: ClassVar[int] = -1
    min_periods: ClassVar[int] = -1


class SeriesFilter(WindowFilter[pd.Series, pd.Series]):
    pass


