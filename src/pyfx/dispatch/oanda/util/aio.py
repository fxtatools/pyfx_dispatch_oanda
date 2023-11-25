"""utility functions for asyncio applications"""

import asyncio as aio
from contextlib import suppress
import concurrent.futures as cofutures
from functools import partial
from typing import Any, Callable, Optional, Union, TYPE_CHECKING
from typing_extensions import TypeAlias, TypeVar


AnyFutureUnion: TypeAlias = Union[cofutures.Future, aio.Future]
AnyFuture = TypeVar("AnyFuture", bound=AnyFutureUnion)


def safe_running_loop() -> Optional[aio.AbstractEventLoop]:
    """Return the running asyncio event loop, or None if no loop is running"""
    with suppress(RuntimeError):
        return aio.get_running_loop()


def set_result_any(future: AnyFuture, value):
    if isinstance(future, cofutures.Future):
        future.set_result(value)
    else:
        if TYPE_CHECKING:
            future: aio.Future
        f_loop = future.get_loop()
        loop = safe_running_loop()
        if loop and loop is f_loop:
            future.set_result(value)
        else:
            _ = f_loop.call_soon_threadsafe(future.set_result, value)


def safe_add_callback(future: AnyFuture, callback: Callable[[AnyFuture], Any]):
    if isinstance(future, aio.Future):
        f_loop = future.get_loop()
        if f_loop is safe_running_loop():
            future.add_done_callback(callback)
        else:
            f_loop.call_soon_threadsafe(future.add_done_callback, callback)
    else:
        future.add_done_callback(callback)


def cancel_when_done(origin, dest):
    if isinstance(dest, cofutures.Future):
        def cancel_cb(dest: cofutures.Future, origin: AnyFuture):
                dest.cancel()
    elif hasattr(dest, "get_loop"):
        def cancel_cb(dest: aio.Future, origin: AnyFuture):
            if dest.done():
                return
            loop = dest.get_loop()
            if loop is safe_running_loop():
                if loop.is_closed():
                    return
                dest.cancel()
            else:
                loop.call_soon_threadsafe(dest.cancel)
    else:
        def cancel_cb(dest, origin):
            dest.cancel()

    cb = partial(cancel_cb, dest)
    safe_add_callback(origin, cb)
    return cb


def chain_cancel_callback(origin: AnyFutureUnion, dest: Union[AnyFutureUnion, aio.Handle]
                          ) -> Callable[[AnyFuture], None]:
    """Bind and return a callback function, cancelling the `dest` future
    when the `origin` future is cancelled.

    The callback function will accept one argument, a future object.
    If the future is cancelled and the `dest` future is not done,
    then the callback will cancel the `dest` future as with
    `dest.cancel()`
    """
    if isinstance(dest, cofutures.Future):
        def cancel_cb(dest: cofutures.Future, origin: AnyFuture):
            if origin.cancelled() and not dest.done():
                dest.cancel()
    elif hasattr(dest, "get_loop"):
        def cancel_cb(dest: aio.Future, origin: AnyFuture):
            if origin.cancelled():
                if dest.done():
                    return
                loop = dest.get_loop()
                if loop is safe_running_loop():
                    if loop.is_closed():
                        return
                    dest.cancel()
                else:
                    loop.call_soon_threadsafe(dest.cancel)
    else:
        def cancel_cb(dest, origin):
            if origin.cancelled():
                dest.cancel()

    cb = partial(cancel_cb, dest)
    safe_add_callback(origin, cb)
    return cb


__all__ = "safe_running_loop", "AnyFutureUnion", "AnyFuture", "safe_add_callback", "cancel_when_done", "chain_cancel_callback"
