# Example API application: Print latest quote information
#
# an alternate approach is illustrated in quotes_async.py

import asyncio as aio
import configparser as cf
from datetime import datetime
import logging
import os
import pyfx.dispatch.oanda as dispatch
import pyfx.dispatch.oanda.logging as dispatch_logging
from pprint import pprint
import sys
from typing import List, Optional


async def run_example(config: dispatch.Configuration) -> List:
    '''print latest quotes for each available instrument in each Account'''
    loop = aio.get_event_loop()
    async with dispatch.ApiClient(loop, config) as api_client:
        api_instance = dispatch.DefaultApi(api_client)
        auth = 'Bearer %s' % config.access_token
        api_response = await api_instance.list_accounts(auth)
        dt_format = config.datetime_format

        accts = api_response.accounts
        for acctinfo in accts:
            id = acctinfo.id
            print("[%s]" % id)
            api_response = await api_instance.get_account_instruments(auth, id)
            instruments = api_response.data.instruments
            instruments.sort(key=lambda inst: inst.name)
            for inst in instruments:
                sys.stdout.write(inst.display_name)
                sys.stdout.write(" ")
                try:
                    api_response = await api_instance.get_instrument_candles(auth, inst.name, count=1)
                    quote = api_response.candles[0]
                    dt = datetime.fromisoformat(quote.time)
                    ohlc = quote.mid
                    print("\to: {0:8s}\th: {0:8s}\tl: {0:8s}\tc: {0:8s}".format(
                        ohlc.o, ohlc.h, ohlc.l, ohlc.c
                    ) + "\t" + dt.strftime(dt_format))
                except dispatch.ApiException:
                    pass

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

    if dbg:
        config.debug = True
    dispatch.Configuration.set_default(config)

    if "TRACE" in os.environ:
        ## optional feature - installing a fault handler for segfaults
        ##
        ## e.g with the IOCP proactor, Python on Windows, a segfault may
        ## occur if the asyncio loop exits abnormally
        logger.info("Loading faulthandler")
        import faulthandler
        faulthandler.enable()

    logger.info("Running example")
    loop = aio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(run_example(config))
    loop.close()
