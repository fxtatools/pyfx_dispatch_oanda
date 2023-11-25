"""GetInstrumentCandles200Response model definition for OANDA v20 REST API (3.0.25)"""

import numpy as np
import pandas as pd
from typing import Annotated

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField

from .candlestick import Candlestick
from .candlestick_granularity import CandlestickGranularity, CandlestickPeriod
from .common_types import InstrumentName, PriceValue, Time

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
        quotes = ("o", "h", "l", "c")
        components = ("mid", "ask", "bid")

        candles = self.candles
        n_candles = len(candles)
        times = np.array([pd.NaT] * n_candles, dtype=Time)
        volume = np.array([0] * n_candles, dtype=int)

        def mk_quote_col(name, n):
            return (name, np.array([np.nan] * n, dtype = PriceValue))

        def mk_component_col(name, n):
            return (name, dict(mk_quote_col(q, n) for q in quotes),)

        abm_map = dict(mk_component_col(component, n_candles) for component in components)

        for n in range(0, n_candles):
            nth = candles[n]
            nth_dct = nth.__dict__
            # if __debug__:
            #     print("-- DEBUG -- nth dct " + repr(nth_dct) )
            volume[n] = nth_dct['volume']
            times[n] = nth_dct['time']
            for component in components:
                nth_component = nth_dct.get(component, None)
                if nth_component is None:
                    if component in abm_map:
                        ## remove the unused data arrays, assuming no later
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
        ## a multi-indexed data frame
        ##
        ## The resulting data frame will contain an "ask", "bid",
        ## and "mid" category within the data frame's multi-index,
        ## for each of those price components in the response quotes,
        ## generally for each price component in the initial request.
        ##
        ## Each price category will present the columns, 'o', 'h',
        ## 'l', and 'c' for each of the open, high, low, and close
        ## quotes for that price category.
        ##
        ## The dataframe will also contain a column for quote volume,
        ## labeled as 'volume' at both levels of the multi-index.
        ##
        ## The index will be a Pandas datetime index.
        ##
        ## An example dataframe can be viewed with [FIXME add example]
        ##
        df_map = {(component, q,): abm_map[component][q] for component in abm_keys for q in quotes}
        vol_label = "volume"
        df_map[(vol_label, vol_label,)] = volume
        ## annotate and return the dataframe
        df: pd.DataFrame = pd.DataFrame(df_map, index=times)
        df.attrs['instrument'] = self.instrument.name
        df.attrs['frequency'] = CandlestickPeriod.get(self.granularity).value
        return df

__all__ = ("GetInstrumentCandles200Response",)
