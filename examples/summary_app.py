# Prototype API application: Print account summary information in the console
#
# This example depends on TaskGroup support, using the
# coroutines-based implementation available in Python 3.11+

import argparse as ap
import asyncio as aio

from pyfx.dispatch.oanda.models import (
    ListAccounts200Response,
    AccountProperties,
    GetAccountSummary200Response,
    AccountSummary,
)

from dataclasses import dataclass, field
import logging
import os
from pyfx.dispatch.oanda.api.default_api import ApiController
import pyfx.dispatch.oanda.util.log as log
from pyfx.dispatch.oanda.util.console_io import console_io
from pyfx.dispatch.oanda.util.paths import expand_path
from pyfx.dispatch.oanda.models.common_types import AccountId
from pyfx.dispatch.oanda.transport.transport_fields import TransportFieldInfo
import sys
from typing import Mapping


logger = logging.getLogger("pyfx.dispatch.oanda.examples")

##
## Application Example for Console - async dispatch via future callbacks
##


@dataclass(eq=False, order=False)
class ExampleController(ApiController):
    processed_lock: aio.Lock = field(init=False, hash=False, default_factory=aio.Lock)

    n_acccounts: int = field(init=False, default=0)
    n_accounts_processed: int = field(init=False, default=0)

    def initialize_defaults(self):
        super().initialize_defaults()
        self.active_accounts = []
        self.processed_lock = aio.Lock()

    def process_args(self, namespace: ap.Namespace, unparsed: list[str]):
        pass

    async def dispatch_summary_display(
        self, future: aio.Future[GetAccountSummary200Response]
    ):
        summary = future.result().account
        fields: list[str] = []
        model_fields: Mapping[str, TransportFieldInfo]  = summary.__class__.model_fields  # type: ignore[assignment]
        for f in model_fields.keys():
            fields.append(f)
        maxlen = max(map(len, fields))
        delim = " : "
        output = sys.stdout
        for field in fields:
            flen = len(field)
            output.write(field)
            output.write(" " * (maxlen - flen))
            output.write(delim)
            print(repr(getattr(summary, field)), file=output)
        async with self.processed_lock:
            self.n_accounts_processed += 1
            if self.n_accounts_processed is self.n_accounts:
                try:
                    self.exit_future.set_result(True)
                except aio.InvalidStateError:
                    pass

    async def call_account_summary(self, account_id: AccountId):
        acct_summary_future: aio.Future[GetAccountSummary200Response] = aio.Future()
        acct_summary_future.add_done_callback(
            self.get_future_callback(self.dispatch_summary_display)
        )
        coro = self.api.get_account_summary(account_id, future=acct_summary_future)
        self.add_task(coro)

    async def dispatch_accounts_summary(
        self, future: aio.Future[ListAccounts200Response]
    ):
        accounts = future.result().accounts
        self.n_accounts = len(accounts)
        for account_props in accounts:
            self.active_accounts.append(account_props)
            account_id = account_props.id
            coro = self.call_account_summary(account_id)
            self.add_task(coro)

    async def run_async(self):
        async with console_io(loop = self.main_loop):
            accounts_future: aio.Future[ListAccounts200Response] = aio.Future()
            accounts_future.add_done_callback(
                self.get_future_callback(self.dispatch_accounts_summary)
            )
            coro = self.api.list_accounts(accounts_future)
            self.add_task(coro)
            await self.exit_future


if __name__ == "__main__":
    ## debug logging will be enabled if DEBUG is set in the environment
    if __debug__ and "DEBUG" in os.environ:
        log.configure_debug_logger()

    cfg_file = expand_path("account.ini", os.path.dirname(__file__))
    if not os.path.exists(cfg_file):
        print("Configuration file not found: %s" % cfg_file, file=sys.stderr)
        sys.exit(1)

    logger.info("Initialzing application")

    with ExampleController.from_args(sys.argv[1:]).run_context() as controller:
        # set a custom datetime format, used in the example
        controller.config.datetime_format = "%a, %d %b %Y %H:%M:%S %Z"
        logger.info("Running example")
