"""GetInstrumentCandles200Response model definition for OANDA v20 REST API (3.0.25)"""

import numpy as np
import pandas as pd
from typing import Annotated, Union

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField

from .candlestick import Candlestick
from .candlestick_granularity import CandlestickGranularity, CandlestickFrequency
from .common_types import InstrumentName, PriceValue, Time
from ..fx_const import FxLabel, FxCol

class GetInstrumentCandles200Response(ApiObject):
    """
    GetInstrumentCandles200Response
    """

    instrument: Annotated[InstrumentName, TransportField(...)]
    """The instrument whose Prices are represented by the candlesticks.
    """

    granularity: Annotated[CandlestickGranularity, TransportField(...)]
    """The granularity of the candlesticks provided.
    """

    candles: Annotated[list[Candlestick], TransportField(...)]
    """The list of candlesticks that satisfy the request.
    """

    def to_df(self) -> pd.DataFrame:

        quotes = (FxLabel.OPEN.value, FxLabel.HIGH.value, FxLabel.LOW.value, FxLabel.CLOSE.value)
        components = (FxLabel.MID.value, FxLabel.ASK.value, FxLabel.BID.value)

        candles = self.candles
        n_candles = len(candles)
        times = np.array([pd.NaT] * n_candles, dtype=Time, copy=False)
        volume = np.array([0] * n_candles, dtype=np.uint32, copy=False)

        def mk_quote_col(name, n):
            # create a column-like tuple containing an array for storing input price values
            #
            # syntax: (<quote_component>, ndarray[double])
            # for <quote_component> one of "o", "h", "l", "c"
            dtype=PriceValue.storage_class
            return (name, np.empty(n, dtype=dtype),)

        def mk_component_col(name, n):
            # create a column-like tuple (<price_component>, <<quote_columns>>)
            # for <price_component> one of "ask", "bid", "mid"
            return (name, dict(mk_quote_col(q, n) for q in quotes),)

        abm_map = dict(mk_component_col(component, n_candles) for component in components)

        for n in range(0, n_candles):
            nth = candles[n]
            nth_dct = nth.__dict__
            volume[n] = nth_dct['volume']
            times[n] = nth_dct['time']
            for component in components:
                nth_component = nth_dct.get(component, None)
                if nth_component is None:
                    if component in abm_map:
                        ## remove unused data arrays, assuming no later
                        ## candlestick objects will have this component
                        del abm_map[component]
                    continue
                else:
                    nth_component_dct = nth_component.__dict__
                    abm_component = abm_map.get(component)
                    for quote in quotes:
                        val = nth_component_dct.get(quote)
                        if __debug__:
                            if not val:
                                raise AssertionError("No value", quote, nth_component)
                        abm_component[quote][n] = val

        abm_keys = tuple(abm_map.keys())
        ## reshape the abm_map price cache, for construction of
        ## a data frame with multi-level columns
        ##
        df_map = {(component, q,): abm_map[component][q] for component in abm_keys for q in quotes}
        df_map[FxCol.VOLUME.value] = volume
        #
        # initialize, annotate, and return the dataframe
        #
        df: pd.DataFrame = pd.DataFrame(df_map, index=pd.DatetimeIndex(times, freq=None), copy=False)
        #
        # ensure the timestamp index is stored in a column
        #
        # Implementation note:
        #
        # to accomodate quotes from partial periods, merging should be conducted
        # on a period index derived from the frequency and timestamps of the quotes,
        # not on the quote timestamp index itself.
        #
        # Regardless, this index here would represent the actual timestamp published
        # by the server, on each quote structure
        #
        timestamp_name = FxLabel.TIME.value
        df.index.name = timestamp_name
        freq =  CandlestickFrequency.get(self.granularity).value.freqstr
        tz = df.index[0].tz

        #
        # The quotes request caller may add any additional metadata.
        #
        # The granularity/frequency and instrument name (enum) are
        # available in this scope.
        #
        # The original request parameters would not be available here,
        # but may be added during request processing
        #
        df.attrs['instrument'] = self.instrument.name
        df.attrs['frequency'] = freq
        df.attrs["granularity"] = self.granularity.value
        df.attrs['tz'] = tz
        return df


__all__ = ("GetInstrumentCandles200Response",)
