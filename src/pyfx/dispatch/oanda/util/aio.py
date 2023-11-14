"""utility functions for asyncio applications"""

import asyncio as aio
from contextlib import suppress
import concurrent.futures as cofutures
from functools import partial
from typing import Callable, Optional, Union
from typing_extensions import TypeAlias, TypeVar


AnyFutureUnion: TypeAlias = Union[cofutures.Future, aio.Future]
AnyFuture = TypeVar("AnyFuture", bound=AnyFutureUnion)


def safe_running_loop() -> Optional[aio.AbstractEventLoop]:
    """Return the running asyncio event loop, or None if no loop is running"""
    with suppress(RuntimeError):
        return aio.get_running_loop()


def chain_cancel_callback(origin: AnyFutureUnion, dest: AnyFutureUnion,
                          dest_concurrent: bool = False) -> Callable[[AnyFuture], None]:
    """Bind and return a callback function, cancelling the `dest` future
    when the `origin` future is cancelled.

    The callback function will accept one argument, a future object.
    If the future is cancelled and the `dest` future is not done,
    then the callback will cancel the `dest` future as with
    `dest.cancel()`

    If `dest_concurrent` is a _falsey_ value (the default) or `dest`
    is not a concurrent future, then the callback will be defined such
    that the `dest` future will be cancelled with a thread-safe call.
    When the callback is dispatched under a running asyncio loop
    other than the `dest` future's asyncio loop and the `dest` future's
    asyncio loop is not closed, the `dest.cancel()`  call will be dispatched
    using `loop.call_soon_threadsafe()` given  `dest.get_loop() == loop`.
    Else, when the callback is dispatched under the same asyncio loop as
    the asyncio future `dest`, then `dest.cancel()` will be called directly.

    When `dest_concurrent` is a _truthy_ value or `dest` is a
    `concurrent.futures.Future`, then the `dest` future will be assumed
    to represent a concurrent future, permitting a direct call to
    `dest.cancel()` from within the calling thread for the callback.

    Before return, the callback function will be bound to the `origin`
    future, using the `add_done_callback` method onto the `origin`
    future.

    The callback function will be returned. For an asyncio `origin` future,
    the return value may be used to remove the callback from the `origin`
    future.
    """
    if dest_concurrent or isinstance(dest, cofutures.Future):
        def cancel_cb(dest: cofutures.Future, origin: AnyFuture):
            if origin.cancelled() and not dest.done():
                dest.cancel()
    else:
        def cancel_cb(dest: aio.Future, origin: AnyFuture):
            loop = dest.get_loop()
            if origin.cancelled():
                if dest.done():
                    return
                if loop is safe_running_loop():
                    if loop.is_closed():
                        return
                    dest.cancel()
                else:
                    loop.call_soon_threadsafe(dest.cancel)

    cb = partial(cancel_cb, dest)
    origin.add_done_callback(cb)
    return cb


__all__ = "safe_running_loop", "AnyFutureUnion", "AnyFuture", "chain_cancel_callback"
