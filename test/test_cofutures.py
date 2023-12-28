"""tests for CoFuture and CoFuturePool"""

from assertpy import assert_that  # type: ignore[import-untyped]
import asyncio as aio
import concurrent.futures as cofutures
from contextlib import suppress
from exceptiongroup import ExceptionGroup
import pytest
from quattro import move_on_after
import sys
import time
from typing import TYPE_CHECKING
from typing_extensions import ClassVar

from pyfx.dispatch.oanda.util.cofuture import CoFuture, CoFuturePool
from pyfx.dispatch.oanda.test import ComponentTest, run_tests


pytest_plugins = ('pytest_asyncio',)


class TestCoFutures(ComponentTest):

    if TYPE_CHECKING:
        xt: ClassVar[cofutures.ThreadPoolExecutor]
        loop: ClassVar[aio.AbstractEventLoop]

    @classmethod
    def setup_class(cls):
        xt = cofutures.ThreadPoolExecutor()
        cls.xt = xt

    def run_threaded(self, func, *args) -> aio.Future:
        return aio.get_running_loop().run_in_executor(self.__class__.xt, func, *args)

    @pytest.mark.asyncio
    async def test_context(self):
        cf = CoFuture(result_value=0)
        delay = sys.getswitchinterval()
        with cf:
            await aio.sleep(delay)
        await cf
        assert_that(cf.result(0)).is_equal_to(0)

    def test_context_folded_exception(self):
        cf = CoFuture(result_value=0)
        exc = ValueError("Passed")
        with suppress(ValueError):
            with cf:
                raise exc

        assert_that(cf.exception()).is_equal_to(exc)

    @pytest.mark.asyncio
    async def test_context_async_folded_exception(self):
        cf = CoFuture(result_value=0)
        exc = ValueError("Passed")
        with suppress(ValueError):
            async with cf:
                raise exc

        assert_that(cf.exception()).is_equal_to(exc)

    def test_context_exception(self):
        cf = CoFuture(result_value=0)
        exc = ValueError("Passed")

        def run_sample(future, exception):
            with future:
                raise exception

        assert_that(run_sample).raises(exc.__class__).when_called_with(cf, exc)
        assert_that(cf.exception()).is_equal_to(exc)

    @pytest.mark.asyncio
    async def test_async_context_exception(self):
        cf = CoFuture(result_value=0)
        exc = ValueError("Passed")

        async def run_coro(future, exception):
            async with future:
                raise exception

        def run_sample(future, exception):
            loop = aio.get_running_loop()
            task = loop.create_task(run_coro(future, exception))
            return task

        received = None
        try:
            task = run_sample(cf, exc)
            await task
        except ValueError as obj:
            received = obj

        assert_that(received).is_equal_to(exc)
        assert_that(cf.exception()).is_equal_to(exc)

    @pytest.mark.asyncio
    async def test_result_threaded(self):
        cf = CoFuture(result_value=0)

        def set_done(delay, future: CoFuture, value):
            time.sleep(delay)
            future.set_result(value)

        delay = sys.getswitchinterval()

        thr_future = self.run_threaded(set_done, delay, cf, 5)

        with suppress(aio.TimeoutError):
            with move_on_after(delay * 4):
                ## aio.timeout N/A in Pyton 3.10 and previous
                await thr_future
                await cf

        assert_that(cf.result(0)).is_equal_to(5)

    @pytest.mark.asyncio
    async def test_pool_future_threaded(self):
        pool = CoFuturePool()
        cf = pool.create_future(result_value=0)

        def set_done(delay, future: CoFuture, value):
            time.sleep(delay)
            future.set_result(value)

        delay = sys.getswitchinterval()

        thr_future = self.run_threaded(set_done, delay, cf, 5)

        with suppress(aio.TimeoutError):
            with move_on_after(delay * 4):
                ## aio.timeout N/A in Pyton 3.10 and previous
                await thr_future
                await cf

        assert_that(cf.result(0)).is_equal_to(5)

    def test_pool_context_exceptions(self):
        exc_0 = ValueError("Passed [0]")
        exc_1 = ValueError("Passed [1]")
        pool = CoFuturePool()

        cf_0 = pool.create_future()
        cf_0.set_exception(exc_0)
        cf_1 = pool.create_future()
        cf_1.set_exception(exc_1)

        grp = None

        try:
            with pool:
                pass
        except ExceptionGroup as exc:
            grp = exc

        assert_that(grp).is_not_none()
        assert_that(exc_0 in grp.exceptions).is_true() # type: ignore[union-attr]
        assert_that(exc_1 in grp.exceptions).is_true() # type: ignore[union-attr]
        assert_that(len(grp.exceptions)).is_equal_to(2) # type: ignore[union-attr]


if __name__ == "__main__":
    run_tests(__file__)
