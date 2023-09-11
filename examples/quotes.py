# Example API application: Print latest quote information

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

def get_abspath(path: os.PathLike, dir_source: Optional[os.PathLike] = None) -> os.PathLike:
    '''utility function for get_config()'''
    if os.path.isabs(path):
        return path
    path = os.path.expanduser(path)
    path_base = dir_source if (dir_source and os.path.isdir(dir_source)) else (
        os.path.dirname(dir_source) if dir_source else os.getcwd())
    path_base = os.path.expanduser(path_base)
    return os.path.abspath(os.path.join(path_base, path))


def get_config(path: os.PathLike, basedir: Optional[os.PathLike] = None) -> dispatch.Configuration:
    '''Parse and return the contents of a configuration file,
as a Configuration object for the API client.

The file should use an INI format, for example:

```
[Configuration]
access_token = <private_token>
host = https://api-fxpractice.oanda.com/v3
```

For purpose of test under the __main__ section below,
the INI file should be located at `account.ini` in
the same directory as this script.

The file should be created with access permissions
limiting all file operations to the creating user.
'''
    pth = get_abspath(path, basedir)
    if not os.path.exists(pth):
        raise RuntimeError("File not found", pth)
    parser = cf.ConfigParser()
    parser.read(pth)
    if 'Configuration' in parser.keys():
        return dispatch.Configuration(**parser['Configuration'])
    else:
        logger.warn("No Configuration section in INI file %s",
                    os.path.abspath(path))
        return dispatch.Configuration()


async def get_account_info(token: str, api: dispatch.DefaultApi) -> List:
    '''API accessor method for list_accounts()'''
    response = await api.list_accounts()
    return response.accounts


async def run_example(config: dispatch.Configuration]) -> List:
    '''print latest quotes for each available instrument in each Account'''
    loop = aio.get_event_loop()
    async with dispatch.ApiClient(loop, config) as api_client:
        api_instance = dispatch.DefaultApi(api_client)
        auth = 'Bearer %s' % config.access_token
        api_response = await api_instance.list_accounts(auth)

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
                    ) + "\t" + dt.strftime("%a, %d %b %Y %H:%M:%S"))
                except dispatch.ApiException:
                    pass

if __name__ == "__main__":
    dispatch_logging.configure_debug_logger()
    logger = logging.getLogger("pyfx.dispatch.oanda")
    logger.info("Loading configuration")
    config = get_config("account.ini", __file__)
    dispatch.Configuration.set_default(config)
    loop = aio.get_event_loop()
    loop.run_until_complete(run_example(config))
    loop.close()
