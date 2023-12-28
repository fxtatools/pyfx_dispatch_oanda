# Prototype API application: Print latest quote information

import argparse as ap
import asyncio as aio

from pyfx.dispatch.oanda.models import (  # type: ignore [attr-defined]
    ListAccounts200Response, AccountProperties,
    GetAccountInstruments200Response, Instrument,
    GetInstrumentCandles200Response
)
from pyfx.dispatch.oanda.transport.account_id import AccountId

from pyfx.dispatch.oanda.models.candlestick_granularity import CandlestickGranularity
from pyfx.dispatch.oanda.models.currency_pair import CurrencyPair
from pyfx.dispatch.oanda.api.price_component import PriceComponent

from contextlib import contextmanager
import logging
import os
from pyfx.dispatch.oanda.api.default_api import ApiController
import pyfx.dispatch.oanda.util.log as log
from pyfx.dispatch.oanda.util import console_io  # type: ignore[attr-defined]
import sys
from typing import Mapping, Optional


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

    instruments_future: aio.Future

    def initialize_defaults(self):
        super().initialize_defaults()
        self.active_accounts = []
        self.instruments = {}
        self.instruments_to_process = set()
        self.n_instruments_processed = 0
        self.processed_lock = aio.Lock()

        inst_future: aio.Future = aio.Future()
        self.instruments_future = inst_future
        exf = self.exit_future
        inst_future.add_done_callback(lambda _: None if exf.done() else exf.set_result(True))

    @classmethod
    @contextmanager
    def argparser(cls, prog: Optional[str] = None, description: Optional[str] = None):
        with super().argparser(prog, description) as parser:
            candles_grp = parser.add_argument_group("candlestick quotes")
            candles_grp.add_argument("-g", "--granularity",
                                     help="Granularity for quotes, i.e timeframe. default: %(default)s",
                                     default="S5", choices=CandlestickGranularity.__members__.keys())
            candles_grp.add_argument("-p", "--price",
                                     help="Price components for quotes, specifying zero or more. default: %(default)s",
                                     choices=("a", "ask", "b", "bid", "m", "mid", "ab", "am", "bm", "abm"),
                                     action="append", default=["m"])
            candles_grp.add_argument("-n", "--count",  type=int,
                                     help="Number of quotes, maximum 5000 per request. default: %(default)s",
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
        inst_info: Instrument = self.instruments[symbol]
        name = CurrencyPair.get(inst_info.display_name).name
        out.write(name)
        granularity = self.quote_granularity
        print(file=out)
        spaces = "    "
        precision = inst_info.display_precision
        dt_tz = self.config.timezone
        dt_fmt = self.config.datetime_format
        for quote in api_response.candles:
            loc_dt = quote.time.astimezone(dt_tz)
            dt_str = loc_dt.strftime(dt_fmt)
            print(spaces + dt_str, file=out)
            for label, field in (("A", "ask"), ("M", "mid"), ("B", "bid")):
                ohlc = getattr(quote, field)
                if not ohlc:
                    continue
                o = ohlc.o
                h = ohlc.h
                l = ohlc.l
                c = ohlc.c
                print(
                    f"{spaces}\t[{granularity:s} {label:s}]     o:{o:^ 12.0{precision}f}  h:{h:^ 12.0{precision}f}  l:{l:^ 12.0{precision}f}  c:{c:^ 12.0{precision}f}",
                    file=out
                )
        async with self.processed_lock:
            self.n_instruments_processed += 1
            if self.n_instruments_processed is self.n_instruments:
                try:
                    self.instruments_future.set_result(True)
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
                coro = self.api.get_instrument_candles(symbol_name.api_name,
                                                       count=self.quotes_count,
                                                       granularity=self.quote_granularity,
                                                       price=self.quote_price,
                                                       future=inst_candles_future)
                task = self.add_task(coro)
                task.add_done_callback(lambda future: inst_candles_future.cancel() if future.cancelled() else None)

    async def call_account_instruments(self, account_id: AccountId):
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
        task = self.add_task(coro)
        task.add_done_callback(lambda future: acct_inst_future.cancel() if future.cancelled() else None)

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
        async with console_io(loop=self.main_loop):
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
            coro = self.api.list_accounts(accounts_future)  # type: ignore
            task = self.add_task(coro)
            task.add_done_callback(lambda future: accounts_future.cancel() if future.cancelled() else None)
            ## ensure the application completes before the async stdio
            ## streams will be closed

            try:
                # await self.exit_future
                await self.instruments_future
            except (aio.CancelledError, aio.InvalidStateError):
                logger.critical("Instruments future cancelled")
                return


if __name__ == "__main__":

    print("-- Initialzing application --")

    with ExampleController.from_args(sys.argv, loop=False).run_context() as controller:

        logger.info("Running example")
        logger.debug("Main loop %r", controller.main_loop)
