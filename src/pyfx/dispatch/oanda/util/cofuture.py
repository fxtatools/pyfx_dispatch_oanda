"""CoFuture and CoFuturePool: Awaitable Concurrent Future, with future grouping support"""

import asyncio as aio
import concurrent.futures as cofutures
from contextlib import suppress
import exceptiongroup
import sys
import threading
import time
from typing import Any, Awaitable, Callable, Generator, Mapping, Optional, Generic, Self, Union, TYPE_CHECKING
from typing_extensions import TypeAlias, TypeVar

from .aio import safe_running_loop


Duration: TypeAlias = Union[int, float]

T = TypeVar("T")


class CoFuture(cofutures.Future[T], Generic[T]):
    if TYPE_CHECKING:
        name: str
        timeout: Duration
        interval: Duration
        result_value: Optional[T]
        result_callback: Optional[Callable[[Self], T]]
        pool: Optional["CoFuturePool"]

    def __init__(self,
                 name: Optional[str] = None, *,
                 pool: Optional["CoFuturePool"] = None,
                 timeout: Optional[Duration] = 0,
                 interval: Optional[Duration] = None,
                 result_value: Optional[T] = None,
                 result_callback: Optional[Callable[[Self], T]] = None
                 ):
        if result_value and result_callback:
            # fmt: off
            raise ValueError("Constructor received both result_value and result_callback", 
                             self, result_value, result_callback)
            # fmt: on
        super().__init__()
        self.name = name or self.__class__.__name__ + "_" + str(id(self))
        switch = sys.getswitchinterval()
        self.timeout = timeout or switch
        self.interval = interval or switch
        self.result_value = result_value
        self.result_callback = result_callback
        if pool:
            pool.enqueue(self)
            ## this would interfere with exception handling in the pool
            # self.add_done_callback(lambda future: pool.dequeue(future))
        self.pool = pool

    async def apoll(self) -> Awaitable[T]:
        timeout = self.timeout
        interval = self.interval
        while True:
            try:
                return self.result(timeout=timeout)
            except TimeoutError:
                await aio.sleep(interval)

    def poll(self) -> T:
        timeout = self.timeout
        interval = self.interval
        while True:
            try:
                return self.result(timeout=timeout)
            except TimeoutError:
                time.sleep(interval)

    def try_set_result(self, result: T) -> bool:
        set_p = False
        with suppress(cofutures.InvalidStateError):
            self.set_result(result)
            set_p = True
        return set_p

    def _repr_state(self) -> str:
        # Known Limitation:
        #
        # This will set any 'accessed' flags for the exception
        # or result attrs
        #
        state = "pending"
        if self.done():
            if self.cancelled():
                state = "cancelled"
            else:
                exc = self.exception(0)
                if exc:
                    state = "raised " + exc.__class__.__name__
                else:
                    result = self.result()
                    state = "returned " + result.__class__.__name__
        return state

    def __repr__(self) -> str:
        return "<%s %s (%s) at 0x%x>" % (
            self.__class__.__name__, self.name,
            self._repr_state(), id(self),
        )

    def __await__(self) -> Generator[Any, None, T]:
        return self.apoll().__await__()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc or exc_type:
            with suppress(cofutures.InvalidStateError):
                self.set_exception(exc or exc_type)
        elif self.done():
            return
        else:
            cb = self.result_callback
            self.set_result(cb(self) if cb else self.result_value)

    async def __aenter__(self) -> Awaitable[Self]:
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return self.__exit__(exc_type, exc, tb)



class CoFuturePool(CoFuture):

    if TYPE_CHECKING:
        pooled: Mapping[cofutures.Future, cofutures.Future]
        pool_lck: threading.RLock

    def __init__(self,
                 name: Optional[str] = None, *,
                 pool: Optional["CoFuturePool"] = None,
                 timeout: Duration = 0,
                 interval: Optional[Duration] = None,
                 result_value: Optional[T] = None,
                 result_callback: Optional[Callable[[Self], T]] = None
                 ):
        super().__init__(
            name, pool=pool, timeout=timeout, interval=interval,
            result_value=result_value, result_callback=result_callback
        )
        ## this would interfere with exceptions under close():
        # self.add_done_callback(lambda _: self.close())
        self.pooled = dict()
        self.pool_lck = threading.RLock()

    def __repr__(self) -> str:
        pool_repr = " ".join(repr(p) for p in self.pooled)
        return "<%s %s (%s) [%s] at 0x%x>" % (
            self.__class__.__name__, self.name,
            self._repr_state(), pool_repr, id(self),
        )

    def create_future(self, *args, **kw) -> CoFuture:
        with self.pool_lck:
            if self.done():
                raise RuntimeError("%s is closed" % self.__class__.__name__)

            kw['pool'] = self
            future = CoFuture(*args, **kw)
            self.pooled[future] = future
            return future

    def enqueue(self, future: cofutures.Future):
        with self.pool_lck:
            if self.done():
                raise RuntimeError("%s is closed" % self.__class__.__name__)
            self.pooled[future] = future
            # if isinstance(future, CoFuture):
            #     future.pool = self

    def dequeue(self, future: cofutures.Future):
        # if __debug__:
        #     if isinstance(future, CoFuture) and future.pool is not self:
        #         raise AssertionError("Future is not assigned to this pool", future, self)
        if future.done():
            exc = None
            removed = False
            with self.pool_lck:
                with suppress(KeyError):
                    del self.pooled[future]
                    removed = True
            if removed:
                with suppress(cofutures.CancelledError, cofutures.TimeoutError):
                    exc = future.exception(self.timeout)
                if exc:
                    raise exc
        else:
            raise ValueError("Future has not completed", future)

    def close(self):
        # process all remaining futures in the pool, cancelling
        # each and gathering exceptions into an exception group
        exc_table = {}
        with self.pool_lck:
            self.cancel()
            interval = self.interval
            for future in self.pooled:
                if future.cancel():
                    #
                    # allow exceptions to propagate
                    # from callbacks
                    #
                    def discard():
                        pass
                    timer = threading.Timer(interval, discard)
                    timer.start()
                    timer.join()
                exc = None
                if future.cancelled():
                    continue
                with suppress(cofutures.CancelledError, cofutures.TimeoutError):
                    exc = future.exception(0)
                if exc and exc not in exc_table:
                    exc_table[exc] = future
        if exc_table:
            raise ExceptionGroup("Exceptions in %r" % self, tuple(exc_table.keys()))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            self.close()
        except ExceptionGroup as eg:
            if exc:
                raise eg from exc
            else:
                raise

    async def __aenter__(self):
        return self.__enter__()

    async def __aexit__(self, exc_type, exc, tb):
        return self.__exit__(exc_type, exc, tb)


__all__ = "Duration", "CoFuture", "CoFuturePool"
