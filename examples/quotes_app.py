# Prototype API application: Print latest quote information
#
# This example depends on TaskGroup support, using the
# coroutines-based implementation available in Python 3.11+

import argparse as ap
import asyncio as aio

from pyfx.dispatch.oanda.models import (  # type: ignore
    ListAccounts200Response, AccountProperties,
    GetAccountInstruments200Response, Instrument,
    GetInstrumentCandles200Response
)

from pyfx.dispatch.oanda.models.candlestick_granularity import CandlestickGranularity
from pyfx.dispatch.oanda.models.currency_pair import CurrencyPair
from pyfx.dispatch.oanda.api.price_component import PriceComponent

from contextlib import contextmanager
import logging
import platform
import os
from pyfx.dispatch.oanda.api.default_api import ApiController
import pyfx.dispatch.oanda.util.log as log
from pyfx.dispatch.oanda.util import expand_path, console_io  # type: ignore
import sys
from typing import Awaitable, Mapping, Optional


logger = logging.getLogger("pyfx.dispatch.oanda.examples")


##
## Application Example for Console - async dispatch via future callbacks
##


class ExampleController(ApiController):

    # fmt: off
    __slots__ = tuple(set(ApiController.__slots__).union(
        "active_accounts", "instruments", "processed_lock",
        "instruments_to_process",  "n_instruments",
        "n_instruments_processed", "args_ns",
        ## slots to initailize from cmdline options
        "quote_granularity", "quote_price", "quotes_count",
        "fetch_instruments"
    ))
    # fmt: on

    active_accounts: list[AccountProperties]
    instruments: Mapping[str, Instrument]

    processed_lock: aio.Lock

    instruments_to_process: set[str]
    n_instruments: int
    n_instruments_processed: int

    args_ns: ap.Namespace

    def initialize_defaults(self):
        super().initialize_defaults()
        self.active_accounts = []
        self.instruments = {}
        self.instruments_to_process = set()
        self.n_instruments_processed = 0
        self.processed_lock = aio.Lock()

    @classmethod
    @contextmanager
    def argparser(cls, prog: Optional[str] = None, description: Optional[str] = None):
        with super().argparser(prog, description) as parser:
            candles_grp = parser.add_argument_group("candlestick quotes")
            candles_grp.add_argument("-g", "--granularity",
                                     help="timeframe i.e Granularity for quotes",
                                     default="S5", choices=CandlestickGranularity.__members__.keys())
            candles_grp.add_argument("-p", "--price",
                                     help="Price component for quotes",
                                     choices=("a", "ask", "b", "bid", "m", "mid", "ab", "am", "bm", "abm"),
                                     action="append", default=["m"])
            candles_grp.add_argument("-n", "--count",  type=int,
                                     help="Number of quotes (maximum: 5000)",
                                     default=1)
            yield parser

    def process_args(self, namespace: ap.Namespace, unparsed: list[str]):
        if len(unparsed) > 0:
            raise ValueError("Unparsed args", unparsed)
        self.quote_granularity = namespace.granularity
        self.quote_price = PriceComponent.get("".join({PriceComponent.get(p) for p in set(namespace.price)}))
        count = namespace.count
        if (count > 5000):
            raise ValueError("Count exceeds protocol limit (5000) for candlestick request", count)
        self.quotes_count = namespace.count

    async def dispatch_candles_display(self, future: aio.Future[GetInstrumentCandles200Response]):
        # Print OHLC data and timestamps from the instrument candles response
        # - presentation function for the console application
        # - in: GetInstrumentCandles200Response, via future callback
        # - process kind: response sink
        api_response = future.result()
        out = sys.stdout
        symbol = api_response.instrument
        inst_info = self.instruments[symbol]
        out.write("%s (%s)" % (inst_info.display_name, self.quote_granularity))
        print(file=out)
        for quote in api_response.candles:
            loc_dt = quote.time.astimezone(self.config.timezone)
            dt_str = loc_dt.strftime(self.config.datetime_format)
            print("    " + dt_str, file=out)
            for label, field in (("A", "ask"), ("M", "mid"), ("B", "bid")):
                ohlc = getattr(quote, field)
                if not ohlc:
                    continue
                o = ohlc.o
                h = ohlc.h
                l = ohlc.l
                c = ohlc.c
                print(
                    "\t  [{0:s}]   o: {1:^9g}\th: {2:^9g}\tl: {3:^9g}\tc: {4:^9g}".format(
                        label, o, h, l, c
                    ),
                    file=out
                )
        async with self.processed_lock:
            self.n_instruments_processed += 1
            if self.n_instruments_processed is self.n_instruments:
                try:
                    self.exit_future.set_result(True)
                except aio.InvalidStateError:
                    pass

    async def dispatch_instrument_candles(self, future: aio.Future[GetAccountInstruments200Response]):
        # for each instrument, create a task to request instrument candles
        # - in: GetAccountInstruments200Response, via future callback
        # - process kind: dispatching request broker
        instruments = future.result().instruments
        async with self.processed_lock:
            self.n_instruments = len(instruments)
        for inst in instruments:
            symbol_name = inst.name
            if symbol_name not in self.instruments_to_process:
                self.instruments[symbol_name] = inst  # type: ignore
                async with self.processed_lock:
                    self.instruments_to_process.add(symbol_name)
                inst_candles_future = aio.Future[GetInstrumentCandles200Response]()
                inst_candles_future.add_done_callback(
                    self.get_future_callback(self.dispatch_candles_display)
                )
                coro = self.api.get_instrument_candles(symbol_name,
                                                       count=self.quotes_count,
                                                       granularity=self.quote_granularity,
                                                       price=self.quote_price,
                                                       future=inst_candles_future)
                self.add_task(coro)

    async def call_account_instruments(self, account_id: str):
        # request a list of instruments available for the account id
        #
        # - in: account_id, via direct call
        # - process kind: dispatching request broker for an iterative request source
        # - general syntax
        #    api.get_account_instruments =[GetAccountInstruments200Response]=> self.dispatch_instrument_candles
        acct_inst_future: aio.Future[GetAccountInstruments200Response] = aio.Future()
        acct_inst_future.add_done_callback(
            self.get_future_callback(self.dispatch_instrument_candles)
        )
        coro = self.api.get_account_instruments(account_id, future=acct_inst_future)
        self.add_task(coro)

    async def dispatch_accounts_instruments(self, future: aio.Future[ListAccounts200Response]):
        # dispatch to call_account_instruments() for each user account
        # - in: API response, via future callback
        # - process kind: dispatching request broker
        # - general syntax
        #   api.list_accounts => [ListAccounts200Response] => self.call_account_instruments
        for account_props in future.result().accounts:
            self.active_accounts.append(account_props)
            account_id = account_props.id
            coro = self.call_account_instruments(account_id)
            self.add_task(coro)

    async def run_async(self):
        async with console_io(self.main_loop):
            # Fetch a list of fxTrade accounts for the requesting client.
            #
            # via future callback: For each account, process each account
            # instrument, to produce each set of candlesticks for display
            # in the script application
            #
            # Known Limitations
            #
            # - This stateless shell script will request the full account
            #   list and instrument details, on each call.
            #
            accounts_future: aio.Future[ListAccounts200Response] = aio.Future()  # type: ignore
            accounts_future.add_done_callback(
                self.get_future_callback(self.dispatch_accounts_instruments)
            )
            coro: Awaitable = self.api.list_accounts(accounts_future)  # type: ignore
            self.add_task(coro)
            ## ensure the application completes before the async stdio
            ## streams will be closed
            await self.exit_future


if __name__ == "__main__":
    ## debug logging will be enabled if DEBUG is set in the environment
    if __debug__ and 'DEBUG' in os.environ:
        log.configure_debug_logger()

    logger.info("Initialzing application")

    if platform.system != "Windows":
        print("Installing uvloop")
        import uvloop
        uvloop.install() # type: ignore[attr-defined]
    with ExampleController.from_args(sys.argv, loop = False).run_context() as controller:
        # set a custom datetime format, used in the example
        controller.config.datetime_format = "%a, %d %b %Y %H:%M:%S %Z"
        logger.info("Running example")
