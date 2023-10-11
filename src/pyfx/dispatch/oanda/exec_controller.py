"""ExecController definition"""

from abc import ABC, abstractmethod
from contextlib import contextmanager, asynccontextmanager
from contextvars import ContextVar
from .configuration import Configuration
from .config_manager import load_config
import asyncio as aio
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from functools import partial
from queue import SimpleQueue
import sys
import time
from types import CoroutineType
from typing import Any, Awaitable, Callable, Optional, Self
from typing_extensions import TypeVar

T = TypeVar("T")

logger = logging.getLogger

thread_loop: ContextVar[aio.AbstractEventLoop] = ContextVar('thread_loop')
"""
Context Variable storage for a primary event loop

Within `ExecController.task_context()` this context variable will
be bound to the controller's primary event loop.

Within threads created under `ExecController.dispatch()` this
context variable will be bound to an event loop initialized
for the thread.

See also:
- ExecController.dispatch()
- ExecController.task_context() [context manager]
"""


@dataclass(eq=False, order=False)
class ExecController(ABC):
    """
    Base class for DispatchController.

    ### Usage

    ExecController provides a generally API-neutral set of
    controller features for asynchronous applications

    - A generalized constructor with support for initialization
      from a configuration file: `ExecController.from_config_ini()`

    - Initialization for a thread pool executor, available mainly
      via `ExecController.dispatch()`

    - Event loop creation for each worker thread, supporting
      asynchronous callbacks at the scope of each thread function

    - Coroutines-based task support within a managed ThreadGroup,
      avaialble via `ExecController.add_task()`

    - General resource cleanup via `close()`

    - Context manager, dispatching to `close()` on exit

    ### Motivation

    This class provides a controller interface without API class dependencies.

    ExecController is extended by DispatchController
    """

    config: Configuration
    """
    Configuration for this controller

    ### Usage

    This Configuration object will be initialized within the generalized
    constructor, `ExecController.from_config_ini()`
    """

    executor: ThreadPoolExecutor = field(hash=False)
    """
    Thread pool executor for this controller

    ### Usage

    This thread pool executor will be created within `initialize_defaults()`
    then defined as the default executor for the controller's main event
    loop.

    This executor is available mainly via `ExecController.dispatch()`
    """

    main_loop: aio.AbstractEventLoop = field(hash=False)
    """
    Main event loop for this controller.

    ### Usage

    This loop may be provided to the ExecController constructor,
    or initialized via an event loop policy
    """

    loop_policy: aio.AbstractEventLoopPolicy
    """
    Policy for event loop creation with this controller

    This policy will be used mainly when creating the event
    loop for each worker thread. The policy may be provided
    to the ExecController constructor
    """

    managed_loops: SimpleQueue[aio.AbstractEventLoop]
    """
    Event loops managed with this controller

    As it representing a stateful queue, this value should
    generally not be modified external to the controller.
    """

    task_group: aio.TaskGroup = field(init=False, hash=False)
    """
    Task group for this controller. Coroutines may be added
    to this task group with the controller method, `add_task()`
    """

    def init_worker_thread(self):
        """
        Worker thread initialization function for the controller's thread pool
        executor

        ### Usage

        This function will be provided as the thread `initializer` function
        for the controller's thread pool executor.

        ### Synopsis

        Create an asyncio event loop for a worker thread, setting that
        loop as the thread's loop and pointing the thread's `thread_loop`
        context variable to that loop.

        The loop should then be available for asynchronous callbacks
        within the thread, via the `thread_loop` context variable, e.g
        `thread_loop.get()`
        """
        ## FIXME on supported platforms, use a uvloop here
        try:
            loop = self.loop_policy.new_event_loop()
            aio.set_event_loop(loop)
            thread_loop.set(loop)
            self.managed_loops.put(loop)
            if __debug__:
                loop.set_debug(sys.platform == "win32")
        except Exception as exc:
            print(exc)
            raise

    def initialize_defaults(self):
        """
        Initialize all default properties for this controller

        - Initialize the controller's thread pool executor,
          using the  `max_thread_workers` property selected
          in this controller's configuration.

        - Initialize an internal loop management queue for
          worker threads

        The executor will be created with an initializer
        calling `init_worker_thread()` for this controller.

        ### Known Limitations

        The worker loop management queue is initialized with
        an asumption that this controller's `close()` function will
        be called within at most one thread.
        """
        max_workers = self.config.max_thread_workers
        exc = ThreadPoolExecutor(max_workers, "exec_",
                                 initializer=self.init_worker_thread)
        self.main_loop.set_default_executor(exc)
        self.executor = exc
        self.managed_loops = SimpleQueue[aio.AbstractEventLoop]()

    @classmethod
    def from_config_ini(cls, path: os.PathLike = "account.ini",
                        loop: Optional[aio.AbstractEventLoop] = None,
                        loop_policy: Optional[aio.AbstractEventLoopPolicy] = None
                        ) -> Self:
        """
        Create an ExecController with a configuration from a provided config ini file

        ## Args

        path: Path to a configuration file for the controller. If provided as a relative
        pathname, the pathname will be interpreted as relative to `os.getcwd()`

        loop: Main event loop for the controller. If not provided, a new event loop will
        be created from the effective event loop policy.

        loop_policy: Event loop policy, if provided. This policy will be used to create
        the main event loop when no loop is provided, as well as for creating the primary
        event loop for each worker thread. If not provided, the default asyncio event
        loop policy will be used.
        """
        inst = cls.__new__(cls)
        config = load_config(path)
        inst.config = config
        _loop_policy = loop_policy or aio.get_event_loop_policy()

        ## TBD integrating uvloop on supported platforms
        inst.loop_policy = _loop_policy
        main_loop = loop or _loop_policy.get_event_loop()
        inst.main_loop = main_loop

        inst.initialize_defaults()
        return inst

    async def dispatch(self, func: Callable[..., T], *args, **kwargs) -> T:
        """
        Dispatch a synchronous function call to a thread worker under this controller

        ### Usage

        The `func` will be called with any provided `args` and/or `kwargs`
        via the thread pool executor for this controller.

        For applications under asynchronous dispatch, the synchronous function
        `func` will be provided with access to an event loop via the binding
        for the `thread_loop` context variable within the containing thread,
        e.g  `thread_loop.get()`
        """
        if len(kwargs) is int(0):
            return await self.main_loop.run_in_executor(self.executor, func, *args)
        else:
            call = partial(func, *args, **kwargs)
            return await self.main_loop.run_in_executor(self.executor, call)

    def close(self):
        """
        Close this controller

        `close()` will perform the following generalized procedure:

        1. Cancel all unfinished tasks under each worker loop,
        also capturing and logging any task exceptions

        2. Close each worker loop

        3. Pause asynchronously for `sys.getswitchinterval()` seconds
        before return, to allow for normal exit under managed tasks
        """
        q = self.managed_loops
        while not q.empty():
            loop = q.get()
            for task in aio.all_tasks(loop):
                task.cancel()
                exc = task.exception()
                if exc:
                    logger.critical(exc)
            loop.close()
        time.sleep(sys.getswitchinterval())

    @abstractmethod
    async def run_async(self):
        raise NotImplementedError(self.run_async)

    def __enter__(self) -> Self:
        """Context manager entry function

        - Initializes the `ExecController.task_context()` for this
          ExecController
        - returns `self` after exit from `run_async()`

        See also: `ExecController.run_context()`
        """
        self.main_loop.run_until_complete(self.run_async())
        return self

    def __exit__(self, *_):
        """Calls `self.close()` before context manager exit"""
        self.close()

    @contextmanager
    def run_context(self):
        """Synchronous context manager for ExecController

        ### Usage

        The context manager method `run_context()` will run the
        `run_async()` method of the implementing ExecController
        within the controller's main loop, after initially yielding
        the controller instance to the implementing context.

        The caller may perform any initial configuration on the
        ExecController instance, while control is yielded to the
        implementing context.

        Before return, the context manager will call `close()`
        on the implementing ExecController

        ### Example

        Given a class `Controller` implementing
        `ExecController.run_async()` and a method `run_pre()`,
        example:

        ```python
        config_file = "config.ini"
        with Controller.from_config_ini(config_file).run_context() as controller:
            controller.run_pre()
            # ... run_async() runs under the controller's main event loop ...
            # ... context manager exits and the controller is closed  ...
        ```
        """
        try:
            yield self
            self.main_loop.run_until_complete(self.run_async())
        finally:
            self.close()

    def add_task(self, coro: CoroutineType) -> aio.Task:
        """
        Create a task to call the provided coroutine `coro` within
        this controller's task group.

        Returns the newly created task
        """
        return self.task_group.create_task(coro)

    def get_future_callback(self, call_to: Callable[..., Awaitable],
                            *args, **kwargs) -> Callable[[aio.Future], Any]:
        """
        Return a callback function for an asyncio Future

        The returned function may be applied as a future callback function, for
        dispatch to a provided coroutine function. The function will accept
        a single arg, assumed to represent a completed aio.Future() object.

        When the returned function is called, then the provided coroutine function
        `call_to` will be called with the future as its first arg. Additional args
        may provided to the couroutine call, via `args` and `kwargs`.

        ## Known Limitations

        It's assumed that the returned callback function will be applied within
        same thread as the executor loop for this controlller
        """
        def future_callback(future):
            nonlocal call_to, args, kwargs
            self.add_task(call_to(future, *args, **kwargs))
        return future_callback

    @asynccontextmanager
    async def task_context(self):
        """Async context manager for ExecController

        ### Usage

        ExecController provides a synchronous context
        manager at the class scope. This context manager
        creates a future to run `ContextManager.run_async()`
        before yielding control to the implementing context.

        The asynchronous `task_context()` context manager
        may applied in `run_async()` implementations

        An example application is avaialble in `quotes_app.py`
        within the `examples` directory

        ### Procedureal Overview

        - Initialize the task group for this controller
        - Bind the current thread's `thread_loop` context variable
        to the main loop for this controller
        """
        async with aio.TaskGroup() as tg:
            self.task_group = tg
            loop_pre = thread_loop.set(self.main_loop)
            try:
                yield self
            finally:
                thread_loop.set(loop_pre)


__all__ = ("thread_loop", "ExecController")
