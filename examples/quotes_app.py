# Prototype API application: Print latest quote information
#
# This example depends on TaskGroup support, using the
# coroutines-based implementation available in Python 3.11+

import asyncio as aio

from pyfx.dispatch.oanda.models import (
    ListAccounts200Response, AccountProperties,
    GetAccountInstruments200Response, Instrument,
    GetInstrumentCandles200Response
)

from dataclasses import dataclass, field
import logging
import os
from pyfx.dispatch.oanda import DispatchController
import pyfx.dispatch.oanda.logging as dispatch_logging
from pyfx.dispatch.oanda.util import expand_path, console_io
import sys
from typing import Awaitable, Mapping, Set


logger = logging.getLogger("pyfx.dispatch.oanda.examples")


##
## Application Example for Console - async dispatch via future callbacks
##

@dataclass(eq=False, order=False)
class ExampleController(DispatchController):
    active_accounts: list[AccountProperties] = field(default_factory=list, repr=False, hash=False)
    instruments: Mapping[str, Instrument] = field(default_factory=dict, repr=False, hash=False)
    instruments_to_process: Set[str] = field(init=False, hash=False)

    def initialize_defaults(self):
        super().initialize_defaults()
        self.active_accounts = []
        self.instruments = {}
        self.instruments_to_process = set()

    async def dispatch_candles_display(self, future: aio.Future[GetInstrumentCandles200Response]):
        # Print OHLC data and timestamps from the instrument candles response
        # - presentation function for the console application
        # - in: GetInstrumentCandles200Response, via future callback
        # - process kind: response sink
        api_response = future.result()
        out = sys.stdout
        symbol = api_response.instrument
        inst_info = self.instruments[symbol]
        self.instruments_to_process.remove(symbol)
        out.write(inst_info.display_name)
        print(file=out)
        for quote in api_response.candles:
            loc_dt = quote.time.astimezone(self.config.timezone)
            dt_str = loc_dt.strftime(self.config.datetime_format)
            print("    " + dt_str, file=out)
            for label, field in (("A", "ask"), ("M", "mid"), ("B", "bid")):
                # Implementation note: New response parser does not store attributes for defaults
                if hasattr(quote, field):
                    ohlc = getattr(quote, field)
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

    async def dispatch_instrument_candles(self, future: aio.Future[GetAccountInstruments200Response]):
        # for each instrument, create a task to request instrument candles
        # - in: GetAccountInstruments200Response, via future callback
        # - process kind: dispatching request broker
        for inst in future.result().instruments:
            symbol_name = inst.name
            if symbol_name not in self.instruments_to_process:
                self.instruments[symbol_name] = inst
                self.instruments_to_process.add(symbol_name)
                inst_candles_future = aio.Future[GetInstrumentCandles200Response]()
                inst_candles_future.add_done_callback(
                    self.get_future_callback(self.dispatch_candles_display)
                )
                coro = self.api.get_instrument_candles(symbol_name, count=3, granularity="M5", price="ABM", future=inst_candles_future)
                self.add_task(coro)

    async def call_account_instruments(self, account_id: str):
        # request a list of instruments available for the account id
        #
        # - in: account_id, via direct call
        # - process kind: dispatching request broker for an iterative request source
        # - general syntax
        #    api.get_account_instruments =[GetAccountInstruments200Response]=> self.dispatch_instrument_candles
        print("[" + account_id + "]")
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
        async with self.task_context():
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
                accounts_future: aio.Future[ListAccounts200Response] = aio.Future()
                accounts_future.add_done_callback(
                    self.get_future_callback(self.dispatch_accounts_instruments)
                )
                coro: Awaitable = self.api.list_accounts(accounts_future)
                await self.add_task(coro)


if __name__ == "__main__":
    ## debug logging will be enabled if DEBUG is set in the environment
    if __debug__ and 'DEBUG' in os.environ:
        dispatch_logging.configure_debug_logger()

    cfg_file = expand_path("account.ini", os.path.dirname(__file__))
    if not os.path.exists(cfg_file):
        print("Configuration file not found: %s" % cfg_file,
              file=sys.stderr)
        sys.exit(1)

    logger.info("Initialzing application")

    with ExampleController.from_config_ini(cfg_file).run_context() as controller:
        # set a custom datetime format, used in the example
        controller.config.datetime_format = "%a, %d %b %Y %H:%M:%S %Z"
        logger.info("Running example")
