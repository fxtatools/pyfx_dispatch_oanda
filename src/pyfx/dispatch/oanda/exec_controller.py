"""ExecController definition"""

from abc import ABC, abstractmethod
from contextlib import contextmanager, asynccontextmanager
from contextvars import ContextVar
from .configuration import Configuration
from .config_manager import load_config
import asyncio as aio
import logging
import os
from concurrent.futures import ThreadPoolExecutor, Executor
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

    - An exit future, available for a non-blocking test before
      exiting the controller main loop process.

    ### Motivation

    This class provides a controller interface without API class dependencies.

    ExecController is extended by DispatchController
    """

    config: Configuration
    """Configuration for this controller

    This Configuration object will be initialized within the
    generalized constructor, `ExecController.from_config_ini()`
    """

    executor: ThreadPoolExecutor = field(hash=False)
    """Thread pool executor for this controller

    An executor may be provied to `from_config_ini()`. If not provided,
    a default ThreadPoolExecutor will be created. The executor will be
    defined as the default executor for the controller's main loop.

    This executor is available mainly via `ExecController.dispatch()`
    """

    main_loop: aio.AbstractEventLoop = field(hash=False)
    """Main event loop for this controller.

    This loop may be provided to the ExecController constructor,
    or initialized via an event loop policy
    """

    loop_policy: aio.AbstractEventLoopPolicy
    """Policy for event loop creation with this controller

    This policy will be applied mainly when creating the event loop for
    each worker thread, and may be applied when creating the exec
    controller's main loop.

    In order to use a custom event loop implementation with the
    exec controller, an event loop policy can be provided to the
    ExecController constructor or `from_config_ini()`
    """

    managed_loops: SimpleQueue[aio.AbstractEventLoop]
    """Event loops managed with this controller

    As representing a stateful queue, this value should
    generally not be modified external to the controller.
    """

    task_group: aio.TaskGroup = field(init=False, hash=False)
    """Task group for this controller.

    Coroutines may be added to this task group with the controller
    method, `add_task()`
    """

    exit_future: aio.Future
    """The exit future for this controller.

    This future will be applied to ensure that any context manager onto
    the exec controller's task group will not return until this future
    has been set to a 'done' state. This is managed mainly via the
    methods, `run_trampoline()` and `await_exit()`, such that would
    be called via the synchronous `run_context()` context manager
    when dispatching to `run_async()` for the implementing class.
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
        if not hasattr(self, "executor"):
            exc = ThreadPoolExecutor(max_workers, "exec_",
                                    initializer=self.init_worker_thread)
            self.executor = exc
        self.main_loop.set_default_executor(self.executor)
        self.managed_loops = SimpleQueue[aio.AbstractEventLoop]()
        if not hasattr(self, "task_group"):
            self.task_group = aio.TaskGroup()
        if not hasattr(self, "exit_future"):
            self.exit_future = aio.Future()

    @classmethod
    def from_config_ini(cls, path: os.PathLike = "account.ini",
                        loop: Optional[aio.AbstractEventLoop] = None,
                        loop_policy: Optional[aio.AbstractEventLoopPolicy] = None,
                        executor: Optional[Executor] = None,
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

        if executor:
            inst.executor = executor

        inst.initialize_defaults()
        return inst


    async def await_exit(self):
        """Await the exit future for this ExecController

        `await_exit()` will return once the exit future for the
        ExecController is set to a 'done' state.

        When this function is provided as a coroutine to a task for the
        ExecController's task group, this should serve to ensure - by
        side effect - that any context manager onto the ExecController's
        task group will not return until the exit future has been set to
        a 'done' state.

        `await_exit()` is added to the exec controller's task group, in
        the default implementation of `ExecController.run_trampoline()`
        """
        try:
            await self.exit_future
        except:
            pass


    async def dispatch(self, func: Callable[..., T], *args, **kwargs) -> T:
        """
        Dispatch a synchronous function call to a threaded worker under this controller

        ### Usage

        The `func` will be called with any provided `args` and/or `kwargs`
        via the thread pool executor for this controller.

        For applications under asynchronous dispatch, the synchronous function
        `func` will be have access to an event loop for the thread, via
        the  binding for the `thread_loop` context variable within the
        containing thread, e.g  `thread_loop.get()`
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
        before return, to allow for normal exit under cancelled tasks
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
        """The primary asynchronous 'run' routine for the exec controller.

        The implementation of `run_async()` will be called from within
        the exec controller's main event loop, such as via the
        synchronous `run_context()` context manager.

        The implementing method should provide any primary application
        logic for the exec controller.

        Additionally, the implementation should ensure that the
        controller's `exit_future` will be set to a 'done' state, at
        some point during the program's runtime.

        An example implementation is avaialble for the DispatchController
        class, in the `examples` sources.
        """
        raise NotImplementedError(self.run_async)

    async def run_trampoline(self):
        """dispatch to run_async() within the contoller's task group context

        ### Synopsis

        This function provides the top-level entry point for dispatch from
        the ExecController's synchronous `run_context()` context manager to
        the implementing class' `run_async()` method.

        In application, `run_trampoline()` will call `run_async()` within
        an asynchronous `task_context()` for the ExecController.

        In effect, this will ensure that all tasks in the ExecController's
        task group will be awaited before return from `run_trampline()`,
        correspondingly before return from `run_context()`.

        ### Exiting the Main Loop

        `run_trampoline()` will add an initial task to the task group
        for the ExecController, such that the task will call the
        coroutine `ExecController.await_exit()` for the exec controller
        instance. The default implementation of `await_exit()` will
        await the `exit_future` for the instance, discarding any
        received exception.

        By side effect, this should serve to ensure that any context
        manager onto the ExecController's task group will not return
        until the `exit_future` for the controller has been set to some
        value, or set to an exception state, or cancelled.

        The implementing class should ensure that the `exit_future` for
        the instance will be set to some value or cancelled at some
        point during the call to `run_async()`, such as once the
        application is in an exit state.
        """
        async with self.task_context():
            self.add_task(self.await_exit())
            await self.run_async()

    @contextmanager
    def run_context(self):
        """Synchronous context manager for ExecController

        ### Usage

        The context manager method `run_context()` will run the
        `run_async()` method of the implementing ExecController
        within the controller's main loop. This will be managed
        directly via the ExecController's `run_trampoline()`
        method.

        Before dispatching to `run_trampoline()`, the controller
        instance will be yielded to the calling context. The caller
        may provide any additional configuration to the ExecController
        instance, at this time, such as within the top-level forms
        of a context manager expression.

        Before return, the context manager will call `close()`
        on the implementing ExecController

        ### Example

        Given a class `Controller` implementing
        `ExecController.run_async()` and a method `run_pre()`, an
        example pattern for application:

        ```python
        config_file = "config.ini"
        with Controller.from_config_ini(config_file).run_context() as controller:
            controller.run_pre()
            # ... run_async() runs under the controller's main event loop ...
            print("Exiting")
            # ... context manager exits and the controller is closed  ...
        ```
        """
        try:
            yield self
            self.main_loop.run_until_complete(self.run_trampoline())
        finally:
            self.close()

    def add_task(self, coro: CoroutineType) -> aio.Task:
        """Task inteface for the exec controller's task group

        `add_task()` will create a task calling the provided
        coroutine `coro` within this exec controller's task
        group.

        Returns the newly created task
        """
        return self.task_group.create_task(coro)

    def get_future_callback(self, call_to: Callable[..., Awaitable],
                            *args, **kwargs) -> Callable[[aio.Future], Any]:
        """Return a callback function for an asyncio Future

        The returned function may be applied as a future callback
        function, for dispatch to a provided coroutine function on
        completion of some aio future. The new function will accept
        a single arg, assumed to represent a completed aio.Future
        object.

        When the function is called, then the provided coroutine function
        `call_to` will be called with the future as its first arg.
        Additional args may provided to the couroutine call, via `args`
        and `kwargs`.

        ## Known Limitations

        It's assumed that the callback function will be applied within
        the same thread as the executor loop for this controlller.
        """
        def future_callback(future):
            nonlocal call_to, args, kwargs
            self.add_task(call_to(future, *args, **kwargs))
        return future_callback

    @asynccontextmanager
    async def task_context(self):
        """Async context manager for ExecController.task_group handling

        ## Usage

        This context manager is applied under ExecController.run_trampoline()

        ## Synopsis

        - Bind the current thread's `thread_loop` context variable to
        the main loop for this controller, within the calling context

        - Await all tasks within the ExecController's task group, before
        return
        """
        tg = self.task_group
        async with tg:
            loop_pre = thread_loop.set(self.main_loop)
            try:
                yield tg
            finally:
                thread_loop.set(loop_pre)


__all__ = ("thread_loop", "ExecController")
