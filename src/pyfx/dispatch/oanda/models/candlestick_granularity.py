"""CandlestickGranularity definition for OANDA v20 REST API (3.0.25)"""

from immutables import Map
import string
from typing import TYPE_CHECKING, Generator, Literal, Union
from typing_extensions import ClassVar, Self
import pandas as pd

from .api_enum import ApiEnum
from ..mapped_enum import  MappedEnum

class CandlestickGranularity(ApiEnum):
    """
    The granularity of a candlestick
    """

    __finalize__: ClassVar[Literal[True]] = True

    S5 = 'S5'
    S10 = 'S10'
    S15 = 'S15'
    S30 = 'S30'
    M1 = 'M1'
    M2 = 'M2'
    M4 = 'M4'
    M5 = 'M5'
    M10 = 'M10'
    M15 = 'M15'
    M30 = 'M30'
    H1 = 'H1'
    H2 = 'H2'
    H3 = 'H3'
    H4 = 'H4'
    H6 = 'H6'
    H8 = 'H8'
    H12 = 'H12'
    D = 'D'
    W = 'W'
    M = 'M'


def _frequency_types() -> Generator[None, None, tuple[str, type[pd.offsets.BaseOffset]]]:
    #
    # generator for FREQUENCY_TYPE_MAP
    #
    # yields values to produce an effective mapping from frequency strings
    # to frequency offset types
    #
    for name in pd.offsets.__all__:
        ref = getattr(pd.offsets, name)
        if isinstance(ref, type) and issubclass(ref, pd.offsets.BaseOffset) and ref is not pd.offsets.BaseOffset:
            try:
                yield ref(1).base.name, ref
            except NotImplementedError:
                pass

FREQUENCY_TYPE_MAP: Map[str, type[pd.offsets.BaseOffset]] = Map(_frequency_types())
# utility value for frequency_alias(), generally appliable for pd.offsets
#
# this value represents a mapping from each offset name string to a
# corresponding offset class - for each offset string produced from
# an offset constructed using default values from the class onto
# ordinal 1 as a constructor arg
#


def frequency_alias(granularity: Union[str, CandlestickGranularity],
                    as_type: bool = False
                    ) -> Union[pd.offsets.BaseOffset, type[pd.offsets.BaseOffset]]:
    #
    # Utility function for the CandlestickFrequency enum value generator
    #
    # Implementation Notes:
    #
    # This function was defined as a simple utility for converting FX granularity
    # names to pandas period offset objects. The application here is closed onto
    # the set of candlestick offset names.
    #
    # When called with as_type = False (default) the resulting objects may generally
    # be applied under the 'freq' arg when creating a Pandas time index.
    #
    # A table of these values is created for each  corresponding FX granularity,
    # in the CandlestickFrequency enum
    #
    # e.g usage
    #
    #  freq = CandlestickFrequency.D.value
    #
    # Known Limitations:
    #
    # - This utility function is not denoted in the module's __all__ index.
    #
    #   The function can be imported directly from the module, however.
    #
    # - This is not a general-purpose frequency name parser.
    #
    #   An overview of the function's limited syntax:
    #
    #   - If the granularity string contains more than one char, each
    #     1+ char will be interpreted as a digit char. This is consistent
    #     with the common syntax for candlestick granuarlity names.
    #
    #   - Generally, "D", "W", and "M"" are supported as single-digit
    #     granularity characters.
    #
    #     "S" and "Y" are also supported, here, however these individual
    #     strings would not be supported under the fxTrade API.
    #
    #     "SD.." would be supported, for "D..." representing a supported
    #      measure of seconds, i.e from {5, 10, 15, 30}
    #
    #   - Absent of a "Business week" offset under Pandas, this uses
    #     the conventional mapping for "W"
    #
    #   - "D" will be parsed as denoting "Business Day"
    #
    #   - Single-char "M" will be parsed as "Business month begin", i.e
    #     colloquially "Business month start" or "BMS" as a freq string
    #
    #   - For "D.."" denoting a sequence of one or more digit chars,
    #     "MD.."  will be parsed as a frquency in minutes.
    #
    #   - Other values will be parsed as generally consistent with the
    #     interpretation under pd.offsets, insofar as represented with
    #     a single-character string in FREQUENCY_TYPE_MAP
    #
    # - Some values returned from this function may not be portable
    #   with pandas.PeiodDtype
    #
    #   Known-incompatible values:
    #
    #   - BusinessMonthBegin cannot typically be used as a frequency
    #     for a pd.PeriodIndex or as frquency for pd.PeriodDtype
    #
    #     However, a BusinessMonthBegin object can be used as a
    #     frequency value under pd.DatetimeIndex
    #
    #     e.g freq = pd.offsets.BusinessMonthBegin(1)
    #
    #     alternately, freq = CandlestickFrequency.M.value
    #
    #   - Similarly, pandas will emit a warning if creating a
    #     pd.PeriodIndex with a freq as a BusinessDay object.
    #     In some later pandas release, it may emit an error.
    #
    #     Regardless, BusinessDay values are also supported
    #     with the 'freq' arg for pd.DatetimeIndex
    #
    #     e.g freq = pd.offsets.BusinessDay(1)
    #
    #     alternately, freq = CandlestickFrequency.D.value
    #
    # docs:
    #
    # frequency offset name part:
    #   https://pandas.pydata.org/docs/user_guide/timeseries.html#timeseries-offset-aliases
    #
    # common aliases:
    #   https://pandas.pydata.org/docs/user_guide/timeseries.html#period-aliases
    #

    label: str = granularity.name if isinstance(granularity, CandlestickGranularity) else granularity

    if len(label) == 1:
        if label == "D":
            # Business Day frequency alias
            return pd.offsets.BusinessDay if as_type else pd.offsets.BusinessDay(1)
        elif label == "M":
            #
            # ambiguous case: "M" can be read as "Minute" or "Month"
            #
            # the fxTrade API does not support multi-month granularity.
            # "M5" would consistently represent "5 minutes"
            #
            # If "M" is received here, it will be parsed as "Month"
            #
            # This uses Business Month Start, in parity with
            # the general interpretation of candlestick times as
            # representing "Open time" for the period denoted of
            # the time value
            #
            return pd.offsets.BusinessMonthBegin if as_type else pd.offsets.BusinessMonthBegin(1)
        elif label == "W":
            # adding another convention here: Week anchored on Monday
            # i.e "W-MON" in pandas-canonical freq strings
            #
            # not necessarily accurate for weeks having a non-trading day on Monday
            #
            return pd.offsets.Week if as_type else pd.offsets.Week(1, weekday=0)
        elif label == "S":
            return pd.offsets.Second if as_type else pd.offsets.Second(1)
        else:
            cls = FREQUENCY_TYPE_MAP.get(label, None)
            if cls is None:
                raise ValueError("Frequency type not found", label)
            else:
                return cls if as_type else cls(1)
    else:
        schar = label[0]
        #
        # with a muliti-character label, "M" will be parsed as "Min"
        #
        # this assumes all chars after label[0] are digit chars
        #
        # for the single usage case of this function returning a type,
        # this makes a recursive call to select the frequency type
        # for the initial FX granularity char
        #
        styp = pd.offsets.Minute if schar == "M" else frequency_alias(schar, as_type=True)
        if as_type:
            return styp
        else:
            return styp(int(label[1:]))


class CandlestickFrequency(MappedEnum):
    """Pandas frequency for each CandlestickGranularity"""

    if TYPE_CHECKING:
        value: pd.offsets.BaseOffset

    __finalize__: ClassVar[Literal[True]] = True

    __gen__ = ((name, frequency_alias(name),) for name in CandlestickGranularity._member_names_)

    @property
    def granularity(self) -> CandlestickGranularity:
        return CandlestickGranularity[self.name]


    @classmethod
    def from_freq(cls, freq: str) -> Self:
        # FIXME add tests
        if freq == "M":
            # Month frequency is represented here with freq for str "BMS"
            return cls.M
        elif freq=="D":
            # Day frequency is represented here with freq for str "B"
            return cls.D
        try:
            return next(v for k, v in cls._value2member_map_.items() if v.value.freqstr == freq)
        except StopIteration:
            raise ValueError("No CandlestickFrequency found", freq)

__all__ = "CandlestickGranularity", "CandlestickFrequency"
