# Example API application: Print latest quote information
#
# requires Python 3.11+
#
# see also: ./quotes_app.py

import argparse as ap
import asyncio as aio

from abc import abstractmethod
from io import IOBase
import logging
import os
import pyfx.dispatch.oanda as dispatch
from pyfx.dispatch.oanda.transport.data import ApiObject
from pyfx.dispatch.oanda.models import GetAccountInstruments200Response, GetInstrumentCandles200Response, CurrencyPair
import pyfx.dispatch.oanda.util.log as log
from pyfx.dispatch.oanda.util.console_io import console_io, ConsoleStreamWriter
from pyfx.dispatch.oanda.api.default_api import ApiController
import pytz
from typing_extensions import Protocol, TypeVar

T = TypeVar("T", bound=ApiObject)


class ConsoleContext(Protocol[T]):
    instream: IOBase
    outstream: IOBase
    errstream: IOBase
    config: dispatch.Configuration
    response: T

    @abstractmethod
    def callback(self, response: T):
        raise NotImplementedError(self.callback)


##
## Async Console Example - function-chain approach
##

class ScriptController(ApiController):

    def process_args(self, namespace: ap.Namespace, unparsed: list[str]):
        pass

    async def run_async(self):
        '''print latest quotes for each available instrument in each Account'''
        loop = aio.get_running_loop()
        config = self.config
        api_instance = self.api
        n_instruments = 0
        n_processed = 0
        processed_lock = aio.Lock()
        instrument_info: dict[str, dispatch.Instrument] = dict()

        async for account_props in api_instance.accounts(self):
            account_id = account_props.id
            dt_format = config.datetime_format
            tz = pytz.timezone(os.environ['TZ']) if 'TZ' in os.environ else config.timezone
            tasks = []

            async with console_io(loop=self.main_loop) as pipe:
                out: ConsoleStreamWriter = pipe.stdout_writer  # type: ignore
                req_grp = self.task_group

                ##
                ## localized task callbacks for instrument->candle
                ## and account->instrument requests
                ##

                async def check_exit():
                    nonlocal n_instruments, n_processed, processed_lock
                    async with processed_lock:
                        n_processed += 1
                        if n_processed == n_instruments:
                            try:
                                self.exit_future.set_result(n_instruments)
                            except aio.InvalidStateError:
                                pass

                def candles_cb(reqftr: aio.Future):
                    nonlocal dt_format, tz, out, instrument_info
                    if reqftr.cancelled():
                        return
                    exc = reqftr.exception()
                    if exc:
                        raise exc
                    api_response: GetInstrumentCandles200Response = reqftr.result()
                    inst: CurrencyPair = api_response.instrument  # type: ignore[assignment]
                    out.write(inst.name)  # type: ignore[attr-defined]
                    print(file=out)
                    for quote in api_response.candles:
                        loc_dt = quote.time.astimezone(tz)
                        dt_str = loc_dt.strftime(dt_format)
                        print("    " + dt_str, file=out)
                        info = instrument_info[api_response.instrument]
                        precision = info.display_precision
                        for component, ohlc in (("A", quote.ask), ("M", quote.mid), ("B", quote.bid)):
                            if ohlc:
                                o = ohlc.o
                                h = ohlc.h
                                l = ohlc.l
                                c = ohlc.c
                                print(
                                    f"\t[{component:s}] o:{o:^ 12.0{precision}f}  h:{h:^ 12.0{precision}f}  l:{l:^ 12.0{precision}f}  c:{c:^ 12.0{precision}f}",
                                    file=out
                                )
                    task = self.add_task(check_exit())
                    self.exit_future.add_done_callback(lambda _: None if task.done() else task.cancel())

                def acct_instrument_cb(reqftr: aio.Future):
                    nonlocal req_grp, api_instance, tasks, account_id, n_instruments, instrument_info
                    if reqftr.cancelled():
                        return
                    exc = reqftr.exception()
                    if exc:
                        raise exc
                    api_response: GetAccountInstruments200Response = reqftr.result()

                    logger.info("response class: %r", api_response.__class__)

                    instruments = api_response.instruments
                    n_instruments = len(instruments)
                    last = None
                    for inst in instruments:
                        iname = inst.name
                        instrument_info[iname] = inst
                        inst_task = self.add_task(
                            api_instance.get_instrument_candles_by_account(account_id,
                                                                           iname,
                                                                           count=5,
                                                                           # granularity = "M1",
                                                                           smooth=False,
                                                                           price=("A", "B", "M",)
                                                                           ))
                        inst_task.add_done_callback(candles_cb)

                ##
                ## Initial Task creation, beginning with each account
                ##

                acct_task = self.add_task(api_instance.get_account_instruments(account_id))
                acct_task.add_done_callback(acct_instrument_cb)
                try:
                    await self.exit_future
                except aio.CancelledError:
                    pass


if __name__ == "__main__":
    ## debug logging will be enabled if DEBUG is set in the environment
    dbg = __debug__ and 'DEBUG' in os.environ
    if dbg:
        log.configure_loggers()
    logger = logging.getLogger("pyfx.dispatch.oanda")
    logger.info("Loading configuration")

    examples_path = dispatch.util.paths.expand_path("account.ini", os.path.dirname(__file__))

    with ScriptController.from_args([]).run_context() as controller:
        ## set a custom datetime format, used in the example
        controller.config.datetime_format = "%a, %d %b %Y %H:%M:%S %Z"
        logger.info("Running example")
        logger.debug("Main loop %r", controller.main_loop)
