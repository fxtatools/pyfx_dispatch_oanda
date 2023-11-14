# Example API application: Print latest quote information
#
# For each instrument available in each client acount,
# OHLC quotes data will fetched and displayed for the
# instrument's latest quote, using default granulatity
# (i.e timeframe)
#
# This example uses a principally synchronous form of
# functional dispatch for request/response processing,
# blocking within each successive request/response cycle.
#
# An alternate approach is illustrated in each of the files
# quotes_async.py and quotes_app.py.
#
# For each example application in this second set of examples,
# the application uses a combination of asyncio futures and
# asynchronous API requests within the application's main
# asyncio event loop. Each API response will then be processed
# using an asynchronous callback under a separate worker thread.
#
# The source code in the following example may provide a more
# succinct illustration of call forms for the API.
#


import asyncio as aio
import argparse as ap
from contextlib import suppress
import sys

from pyfx.dispatch.oanda.api.default_api import ApiController


class ExampleController(ApiController):
    def process_args(self, namespace: ap.Namespace, unparsed: list[str]):
        pass

    async def run_async(self):
        api = self.api
        api_response = await api.list_accounts()

        accts = api_response.accounts
        for acctinfo in accts:
            id = acctinfo.id
            print("[%s]" % id)
            api_response = await api.get_account_instruments(id)
            instruments = api_response.instruments
            instruments.sort(key=lambda inst: inst.name)
            out = sys.stdout
            for inst in instruments:
                api_response = await api.get_instrument_candles(inst.name, count=1)
                out.write(inst.display_name)
                out.write(" ")
                quote = api_response.candles[0]
                mid = quote.mid
                precision = inst.display_precision
                o = mid.o
                h = mid.h
                l = mid.l
                c = mid.c
                out.write(
                    f" o:{o:^ 12.0{precision}f}  h:{h:^ 12.0{precision}f}  l:{l:^ 12.0{precision}f}  c:{c:^ 12.0{precision}f} ",
                )
                print(quote.time.strftime(self.config.datetime_format), file=out)

        with suppress(aio.InvalidStateError):
            self.exit_future.set_result(True)


if __name__ == "__main__":
    with ExampleController.from_args(sys.argv, loop=False).run_context() as controller:
        logger = controller.logger
        logger.info("Running example")
