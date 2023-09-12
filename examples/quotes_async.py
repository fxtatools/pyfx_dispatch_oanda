# Example API application: Print latest quote information

import asyncio as aio

from datetime import datetime
import logging
import os
import pyfx.dispatch.oanda as dispatch
import pyfx.dispatch.oanda.logging as dispatch_logging
from pyfx.dispatch.oanda.util import console_io, ConsoleStreamWriter
import re
from typing_extensions import List


##
## Async Console Example
##

async def run_example(config: dispatch.Configuration) -> List:
    '''print latest quotes for each available instrument in each Account'''
    loop = aio.get_event_loop()
    async with dispatch.ApiClient(loop, config) as api_client:
        api_instance = dispatch.DefaultApi(api_client)
        auth = 'Bearer %s' % config.access_token
        api_response = await api_instance.list_accounts(auth)
        dt_format = config.datetime_format

        accts = api_response.accounts
        tasks = []

        async with console_io(loop) as pipe:
            out: ConsoleStreamWriter = pipe.stdout_writer
            async with aio.TaskGroup() as req_grp:

                ##
                ## localized task callbacks for instrument->candle*
                ## and account->instrument* requests
                ##

                def candles_cb(reqftr: aio.Future):
                    nonlocal dt_format, out
                    if reqftr.cancelled():
                        return
                    exc = reqftr.exception()
                    if exc:
                        raise exc
                    api_response: dispatch.GetInstrumentCandles200Response = reqftr.result()
                    out.write(re.sub("_", "/", api_response.instrument, count=1))
                    out.write(" ")
                    quote = api_response.candles[0]
                    dt = datetime.fromisoformat(quote.time)
                    ohlc = quote.mid
                    print("\to: {0:8s}\th: {0:8s}\tl: {0:8s}\tc: {0:8s}".format(
                        ohlc.o, ohlc.h, ohlc.l, ohlc.c
                    ) + "\t" + dt.strftime(dt_format), file=out)

                def inst_cb(reqftr: aio.Future):
                    nonlocal req_grp, api_instance, auth, tasks
                    if reqftr.cancelled():
                        return
                    exc = reqftr.exception()
                    if exc:
                        raise exc
                    api_response: dispatch.GetAccountInstruments200Response = reqftr.result()
                    instruments = api_response.data.instruments
                    instruments.sort(key=lambda inst: inst.name)
                    for inst in instruments:
                        task = req_grp.create_task(api_instance.get_instrument_candles(auth, inst.name, count=1, smooth=False))
                        task.add_done_callback(candles_cb)
                        tasks.append(task)

                ##
                ## Initial Task creation, beginning with each account
                ##
                for acctinfo in accts:
                    id = acctinfo.id
                    task = req_grp.create_task(api_instance.get_account_instruments(auth, id))
                    task.add_done_callback(inst_cb)
                    tasks.append(task)
                    print("[%s]" % id)

                ## Return a Future object, such that the future's result value
                ## will represent the set of results for tasks created here
                return await aio.gather(*tasks, return_exceptions=True)

if __name__ == "__main__":
    ## debug logging will be enabled if DEBUG is set in the environment
    dbg = __debug__ and 'DEBUG' in os.environ
    if dbg:
        dispatch_logging.configure_debug_logger()
    logger = logging.getLogger("pyfx.dispatch.oanda")
    logger.info("Loading configuration")

    ## initialize the configuration object
    examples_cfg = dispatch.util.paths.expand_path("account.ini", os.path.dirname(__file__))
    config = dispatch.config_manager.load_config(examples_cfg)
    dispatch.Configuration.set_default(config)

    ## set a custom datetime format, used in the example
    config.datetime_format = "%a, %d %b %Y %H:%M:%S %Z"
    logger.info("Running example")

    if "TRACE" in os.environ:
        ## optional feature - installing a fault handler for segfaults
        ##
        ## e.g with the IOCP proactor, Python on Windows, a segfault may
        ## occur if the asyncio loop exits abnormally
        logger.info("Loading faulthandler")
        import faulthandler
        faulthandler.enable()

    loop = aio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(run_example(config))
    loop.close()
