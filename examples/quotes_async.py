# Example API application: Print latest quote information
#
# requires Python 3.11+
#
# see also: ./quotes_app.py

import asyncio as aio

from abc import abstractmethod
from io import IOBase
import logging
import os
import pyfx.dispatch.oanda as dispatch
import pyfx.dispatch.oanda.logging as dispatch_logging
from pyfx.dispatch.oanda.util import console_io, ConsoleStreamWriter
from pyfx.dispatch.oanda.api.default_api import DispatchController
import pytz
import re
from typing_extensions import Protocol, TypeVar

T = TypeVar("T", bound=dispatch.ApiObject)


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

class ScriptController(DispatchController):

    async def run_async(self):
        '''print latest quotes for each available instrument in each Account'''
        controller = self
        loop = aio.get_running_loop()
        config = controller.config
        api_instance = controller.api

        async for account_props in api_instance.accounts(controller):
            account_id = account_props.id
            dt_format = config.datetime_format
            tz_str = os.environ['TZ'] if 'TZ' in os.environ else config.timezone
            tz = pytz.timezone(tz_str)
            tasks = []

            async with console_io(loop) as pipe:
                out: ConsoleStreamWriter = pipe.stdout_writer
                req_grp = self.task_group

                ##
                ## localized task callbacks for instrument->candle*
                ## and account->instrument* requests
                ##

                def candles_cb(reqftr: aio.Future):
                    nonlocal dt_format, tz, out
                    if reqftr.cancelled():
                        return
                    exc = reqftr.exception()
                    if exc:
                        raise exc
                    api_response: dispatch.GetInstrumentCandles200Response = reqftr.result()
                    out.write(re.sub("_", "/", api_response.instrument, count=1))
                    print(file=out)
                    for quote in api_response.candles:
                        loc_dt = quote.time.astimezone(tz)
                        dt_str = loc_dt.strftime(dt_format)
                        print("    " + dt_str, file=out)
                        for name, ohlc in (("A", quote.ask), ("M", quote.mid), ("B", quote.bid)):
                            if ohlc:
                                o = ohlc.o
                                h = ohlc.h
                                l = ohlc.l
                                c = ohlc.c
                                print(
                                    "\t  [{0:s}]   o: {1:^9g}\th: {2:^9g}\tl: {3:^9g}\tc: {4:^9g}".format(
                                        name, o, h, l, c
                                    ),
                                    file=out
                                )

                def acct_instrument_cb(reqftr: aio.Future):
                    nonlocal req_grp, api_instance, tasks, account_id
                    if reqftr.cancelled():
                        return
                    exc = reqftr.exception()
                    if exc:
                        raise exc
                    api_response: dispatch.GetAccountInstruments200Response = reqftr.result()

                    logger.info("response class: %r", api_response.__class__)

                    instruments = api_response.instruments
                    last = None
                    for inst in instruments:
                        inst_task = self.add_task(
                            api_instance.get_instrument_candles_by_account(account_id,
                                                                            inst.name,
                                                                            count=5,
                                                                            # granularity = "M1",
                                                                            smooth=False,
                                                                            price="ABM"
                                                                            ))
                        inst_task.add_done_callback(candles_cb)
                        last = inst_task
                    ## Implementation note: Though the last task created here may not be
                    ## the last task to exit, setting the 'done' state during the last
                    ## task's completion here should serve to ensure that the 'done' state
                    ## is set, not until there are already a number of tasks in the task
                    ## group. It will not cause the task group to exit immediately, simply
                    ## indicating that the controller is in a closeable state.
                    ##
                    ## This is really a bit of a hack. Considering that the list of
                    ## instruments to fetch is not recorded here except for purpose
                    ## of dispatching to fetch instrument candles, the number of remaining
                    ## instruments for OHLC sets to fetch cannot be determined here.
                    ##
                    ## Although not by any exactly deterministic event flow, generally
                    ## it "Just works," to set the exit_future to 'done', within this
                    ## callback
                    ##
                    last.add_done_callback(lambda ftr: self.exit_future.set_result(True))


                ##
                ## Initial Task creation, beginning with each account
                ##

                acct_task = self.add_task(api_instance.get_account_instruments(account_id))
                acct_task.add_done_callback(acct_instrument_cb)
                await self.exit_future


if __name__ == "__main__":
    ## debug logging will be enabled if DEBUG is set in the environment
    dbg = __debug__ and 'DEBUG' in os.environ
    if dbg:
        dispatch_logging.configure_debug_logger()
    logger = logging.getLogger("pyfx.dispatch.oanda")
    logger.info("Loading configuration")

    examples_path = dispatch.util.paths.expand_path("account.ini", os.path.dirname(__file__))
    with ScriptController.from_config_ini(examples_path).run_context() as controller:
        ## set a custom datetime format, used in the example
        controller.config.datetime_format = "%a, %d %b %Y %H:%M:%S %Z"
        logger.info("Running example")
