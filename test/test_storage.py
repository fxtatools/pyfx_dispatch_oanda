"""Unit tests for Api Object Storage"""

import ijson  # type: ignore[import-untyped]
import os
from pathlib import Path
import pytest

import ZODB  # type: ignore[import-untyped]
from zope.password.password import SHA1PasswordManager  # type: ignore[import-untyped]

from pyfx.dispatch.oanda.test import ComponentTest, run_tests, assert_recursive_eq
from pyfx.dispatch.oanda.util.paths import expand_path, Pathname
from pyfx.dispatch.oanda.app.storage_controller import shadow_encoder

from pyfx.dispatch.oanda.parser import ModelBuilder
from pyfx.dispatch.oanda.transport.data import ApiObject, JsonTypesRepository
from pyfx.dispatch.oanda.io import AsyncSegmentChannel
from pyfx.dispatch.oanda.models import (
    ListAccounts200Response,
    GetAccount200Response,
    GetAccountSummary200Response,
    GetAccountInstruments200Response,
    GetInstrumentCandles200Response,
    GetTransactionRange200Response,
    ListOrders200Response,
    ListTrades200Response
)

## FIXME partially duplicating ./test_parse_unparse.py

pytest_plugins = ('pytest_asyncio',)

SAMPLES_DIR: Pathname = os.path.abspath(os.path.join(os.path.dirname(__file__),  "sample_data"))


@pytest.fixture
## docs https://docs.pytest.org/en/7.1.x/how-to/tmp_path.html
def zodb_fs_file(tmp_path_factory) -> Path:
    ## initialize ZODB file storage at some temporary pathname
    fs_path = tmp_path_factory.mktemp("test_storage") / "zodb.fs"
    db = ZODB.DB(str(fs_path))
    db.open()
    db.close()
    return fs_path


class TestStorage(ComponentTest):

    async def run_builder_async(self, cls: type[ApiObject], samples_dir: Pathname) -> ApiObject:
        JsonTypesRepository.__finalize_instance__()

        example_file = expand_path(cls.__name__ + ".json", samples_dir)
        if not os.path.exists(example_file):
            raise ValueError("No example file found", example_file)

        return await cls.afrom_file(example_file)

    @pytest.fixture
    def samples_dir(self) -> Pathname:
        return SAMPLES_DIR

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "model_cls", [
            ListAccounts200Response,
            GetAccount200Response,
            GetAccountSummary200Response,
            GetAccountInstruments200Response,
            GetInstrumentCandles200Response,
            GetTransactionRange200Response,
            ListOrders200Response,
            ListTrades200Response
        ]
    )
    async def test_storage(self, model_cls: type[ApiObject], samples_dir: Pathname, zodb_fs_file: Path):
        fs_filename = str(zodb_fs_file)

        #
        # ensure a credential shadow encoder is available in the environment
        #

        shadow_encoder.set(SHA1PasswordManager())

        #
        # parse the sample file
        #

        instance = await self.run_builder_async(model_cls, samples_dir)

        #
        # test storage, deserialization within the same db session
        #

        db = ZODB.DB(fs_filename)
        try:
            with db.transaction() as conn:
                conn.root.instance = instance

            with db.transaction() as conn:
                deserialized = conn.root.instance

            assert_recursive_eq(deserialized, instance)
        finally:
            db.close()

        #
        # test under a new db session
        #

        db_next = ZODB.DB(fs_filename)

        try:
            with db_next.transaction() as conn:
                deserialized_after_close = conn.root.instance

            assert_recursive_eq(deserialized_after_close, instance)
        finally:
            db_next.close()

        #
        # cleanups for the testing environment
        #

        fs_dir = zodb_fs_file.parent
        for file in fs_dir.glob("*"):
            file.unlink()
        fs_dir.rmdir()


if __name__ == "__main__":
    run_tests(__file__)
