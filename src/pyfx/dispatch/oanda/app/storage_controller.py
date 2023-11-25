"""Storage support for ExecController/RequestController applications - base classes"""

from abc import ABC, abstractmethod
import argparse as ap
from contextlib import contextmanager, asynccontextmanager
from contextvars import ContextVar
import logging
import os
from pathlib import Path
from typing import Iterator, Optional
from transaction import TransactionManager  # type: ignore[import-untyped]
import ZODB  # type: ignore[import-untyped]
from ZODB.Connection import Connection  # type: ignore[import-untyped]
from ZODB.FileStorage import FileStorage  # type: ignore[import-untyped]
from zope.password.interfaces import IPasswordManager  # type: ignore[import-untyped]
from zope.password.password import SHA1PasswordManager  # type: ignore[import-untyped]

from ..api.request_base import RequestController
from ..credential import shadow_encoder

logger = logging.getLogger(__name__)

thread_controller: ContextVar["StorageController"] = ContextVar("thread_controller")


class StorageController(RequestController, ABC):
    __slots__ = tuple(
        list(RequestController.__slots__) + [
            "db_path", "db",  "shadow_encoder"
        ])

    db_path: Path
    db: ZODB.DB
    shadow_encoder: IPasswordManager

    @classmethod
    def get_default_db_filename(cls):
        appdirs = cls.appdirs
        return os.path.join(appdirs.user_data_dir, "zodb.fs")

    @classmethod
    @contextmanager
    def argparser(
        cls, prog: Optional[str] = None, description: Optional[str] = None
    ) -> Iterator[ap.ArgumentParser]:
        with super().argparser(prog, description) as parser:
            storage_grp = parser.add_argument_group("storage")
            storage_grp.add_argument("-f", "--file", dest="db_filename",
                                     default=cls.get_default_db_filename(),
                                     help="Custom path for database file")
            yield parser

    def process_args(self, namespace: ap.Namespace, unparsed: list[str]):
        self.db_path = Path(os.path.abspath(namespace.db_filename))

    def initialize_defaults(self):
        super().initialize_defaults()
        ## tested initially, does not yield consistent shadow values
        # self.shadow_encoder = BCRYPTPasswordManager()
        ## the SHA1 and MD5 encoders produce consistent output
        self.shadow_encoder = SHA1PasswordManager()

    def init_worker_thread(self):
        super().init_worker_thread()
        thread_controller.set(self)
        shadow_encoder.set(self.shadow_encoder)

    @abstractmethod
    def bind_schema(self):
        raise NotImplementedError(self.bind_schema)

    def ensure_db(self):
        if not hasattr(self, "db"):
            # Implementation Notes
            #
            # - the file at db_path will be accompanied with
            #   a number of additional files in the same
            #   directory. These files will generally have
            #   the same pathname stem, with differing file
            #   type/file name extension.
            #
            # - ZODB FileStorage() ctor will create the storage
            #   files automatically, if the files did not exist.
            #
            #
            db_path = self.db_path
            db_dir = db_path.parent
            if not db_dir.exists():
                db_dir.mkdir(parents=True)
            if __debug__:
                logger.debug("Initializing DB: %r ", db_path)
            fs = FileStorage(str(db_path))
            ## needed for applications, may interfere with
            ## at-a-glance review of ZODB FS data
            # zc_storage = ZlibStorage(fs)
            # db = ZODB.DB(zc_storage)
            db = ZODB.DB(fs)
            self.db = db

        self.bind_schema()

    @asynccontextmanager
    async def async_context(self):
        async with super().async_context() as supra:
            try:
                ctrl = thread_controller.set(self)
                enc = shadow_encoder.set(self.shadow_encoder)
                self.ensure_db()
                yield supra
            finally:
                thread_controller.reset(ctrl)
                shadow_encoder.reset(enc)

    def close(self, immediate: bool = False):
        if hasattr(self, "db"):
            db = self.db
            if __debug__:
                logger.debug("Closing DB: %r", db)
            for conn in db.pool:
                ## close remaining transactions
                conn.close()
            self.db.close()
        super().close(immediate)

    @contextmanager
    def db_transaction(self) -> Iterator[Connection]:
        mgr = TransactionManager()
        txn = mgr.begin()
        conn = None
        try:
            conn: Connection = self.db.open(mgr)
            yield conn
        except Exception as exc:
            txn.abort()
            raise RuntimeError("Error during transaction", conn) from exc
        else:
            txn.commit()
        finally:
            if conn:
                conn.close()
