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

    async def poll(self) -> Awaitable[T]:
        timeout = self.timeout
        interval = self.interval
        while True:
            try:
                return self.result(timeout=timeout)
            except TimeoutError:
                await aio.sleep(interval)

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
        return self.poll().__await__()

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

    def get_loop(self):
        # portability shim
        return safe_running_loop() or aio.get_event_loop_policy().get_event_loop()


class CoFuturePool(CoFuture):

    if TYPE_CHECKING:
        pooled: list[cofutures.Future]
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
        self.pooled = []
        self.pool_lck = threading.RLock()

    def __repr__(self) -> str:
        pool_repr = " ".join(repr(p) for p in self.pooled)
        return "<%s %s (%s) [%s] at 0x%x>" % (
            self.__class__.__name__, self.name,
            self._repr_state(), pool_repr, id(self),
        )

    def future(self, *args, **kw) -> CoFuture:
        with self.pool_lck:
            if self.done():
                raise RuntimeError("%s is closed" % self.__class__.__name__)

            kw['pool'] = self
            future = CoFuture(*args, **kw)
            self.pooled.append(future)
            return future

    def enqueue(self, future: cofutures.Future):
        with self.pool_lck:
            if self.done():
                raise RuntimeError("%s is closed" % self.__class__.__name__)
            self.pooled.append(future)
            # if isinstance(future, CoFuture):
            #     future.pool = self

    def dequeue(self, future: cofutures.Future):
        # if __debug__:
        #     if isinstance(future, CoFuture) and future.pool is not self:
        #         raise AssertionError("Future is not assigned to this pool", future, self)
        if future.done():
            exc = None
            with self.pool_lck:
                with suppress(ValueError):
                    self.pooled.remove(future)
            with suppress(cofutures.CancelledError, cofutures.TimeoutError):
                exc = future.exception(self.timeout)
            if exc:
                raise exc
        else:
            raise ValueError("Future has not completed", future)

    def close(self):
        exception_unique = set()
        exceptions_ordered = []
        with self.pool_lck:
            self.cancel()
            pooled = self.pooled
            if pooled:

                def discard(_):
                    pass
                interval = self.interval
                for future in pooled.copy():
                    #
                    # this assumes that the future is done
                    # or in a cancellable state
                    #
                    if future.cancel():
                        #
                        # allow exceptions to propagate
                        # from callbacks
                        #
                        timer = threading.Timer(interval, lambda: _)
                        timer.join()
                    with exceptiongroup.catch({
                        cofutures.TimeoutError: discard,
                        cofutures.CancelledError: discard,
                        Exception: exceptions_ordered.append
                    }):
                        exc = future.exception()
                        if exc:
                            if exc not in exception_unique:
                                exceptions_ordered.append(exc)
                                exception_unique.add(exc)
                        else:
                            _ = future.result(self.timeout)
                    with suppress(ValueError):
                        pooled.remove(future)
        if exceptions_ordered:
            raise ExceptionGroup("Exceptions in %r" % self, exceptions_ordered)

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
