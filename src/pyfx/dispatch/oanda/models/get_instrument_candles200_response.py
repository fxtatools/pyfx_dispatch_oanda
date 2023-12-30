"""GetInstrumentCandles200Response model definition for OANDA v20 REST API (3.0.25)"""

import numpy as np
import pandas as pd
from collections.abc import Mapping
from typing import Annotated, Optional, Union
from typing_extensions import TypeAlias

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
        times = np.empty(n_candles, dtype=Time)
        volume = np.empty(n_candles, dtype=np.uint32)
        complete_data = np.empty(n_candles, dtype=np.bool_)

        def mk_quote_col(name, n):
            # create a column-like tuple containing an array for storing input price values
            #
            # syntax: (<quote_component>, ndarray[double])
            # for <quote_component> one of "o", "h", "l", "c"
            dtype = PriceValue.storage_class
            return (name, np.empty(n, dtype=dtype),)

        def mk_component_col(name, n):
            # create a column-like tuple (<price_component>, <<quote_columns>>)
            # for <price_component> one of "ask", "bid", "mid"
            return (name, dict(mk_quote_col(q, n) for q in quotes),)

        abm_map = dict(mk_component_col(component, n_candles) for component in components)

        for n in range(0, n_candles):
            nth = candles[n]
            nth_fields = nth.__dict__
            volume[n] = nth_fields['volume']
            times[n] = nth_fields['time']
            complete_data[n] = nth_fields['complete']
            for component in components:
                nth_component = nth_fields.get(component, None)
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
        #
        # reshape the abm_map price cache, for construction of
        # a data frame with multi-level columns
        #
        df_map = {(component, q,): abm_map[component][q] for component in abm_keys for q in quotes}
        #
        # add comopnent-generic columns
        #
        df_map[FxCol.VOLUME.value] = volume
        df_map[FxCol.COMPLETE] = complete_data
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

        ## Revised: add period later, if used for merge
        freq = CandlestickFrequency.get(self.granularity).value.freqstr
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

LatestQuotesMap: TypeAlias = Mapping[InstrumentName, Mapping[CandlestickGranularity, pd.DataFrame]]


class GetAccountCandlesLatest200Response(ApiObject):
    latest_candles: Annotated[
        list[GetInstrumentCandles200Response],
        TransportField(
            ..., alias="latestCandles",
            description="""Latest candlestick data, per request candle specifications"""
        )]

    def to_df_map(self) -> LatestQuotesMap:
        # produce a mapping of instrument, granularity, dataframe objects
        # for dataframes derived from the union of price components for
        # each instrument, granularity in the response.

        latest_map: LatestQuotesMap = dict()

        components = (FxLabel.MID.value, FxLabel.ASK.value, FxLabel.BID.value)
        components_s = frozenset(components)

        for quotes in self.latest_candles:
            #
            # process each set of candles in the response
            #
            inst = quotes.instrument
            granularity = quotes.granularity

            inst_table: Optional[Mapping[CandlestickGranularity, pd.DataFrame]] = latest_map.get(inst, None)
            inst_new: bool = False
            data_new: bool = False
            if inst_table is None:
                inst_table = dict()
                inst_new = True
                latest_map[inst] = inst_table

            mapped_df: Optional[pd.DataFrame] = inst_table.get(granularity, None) if inst_new is False else None
            if mapped_df is None:
                data_new = True

            df = quotes.to_df()

            if data_new is True:
                inst_table[granularity] = df
            else:
                #
                # add any nonexistent component data (ask, bid, mid quotes)
                #
                diff = components_s.difference(frozenset(df.columns))
                for co in sorted(diff):
                    mapped_df.loc[:, co] = df.loc[:, co]

        return latest_map


__all__ = ("GetInstrumentCandles200Response",)
