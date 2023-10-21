"""ExecController definition"""

from abc import ABC, abstractmethod
from appdirs import AppDirs
import argparse as ap
import asyncio as aio
from contextlib import contextmanager, asynccontextmanager
from contextvars import ContextVar
from .configuration import Configuration
from .config_manager import load_config
from .util.paths import Pathname, expand_path
import logging
import persistent
import os
import stat

from concurrent.futures import ThreadPoolExecutor, Executor
import concurrent.futures as cofutures
from dataclasses import dataclass, field
from functools import partial
from prompt_toolkit import prompt
from queue import SimpleQueue
import sys
import time
import traceback
from types import CoroutineType
from typing import (
    Any,
    Awaitable,
    Callable,
    Collection,
    Generic,
    Iterator,
    Literal,
    Mapping,
    Optional,
    Self,
    Union,
)
from typing_extensions import ClassVar, TypeVar

from .util.dist import find_distribution, PackageNotFoundError
from .util.args import argparser, subparsers, command_parser


T = TypeVar("T")

logger: logging.Logger = logging.getLogger(__name__)

thread_loop: ContextVar[aio.AbstractEventLoop] = ContextVar("thread_loop")
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


class ExecController(ABC):
    """
    Base class for ApiController

    ### Usage

    ExecController provides a generally API-neutral set of
    controller features for asynchronous applications

    - A generalized constructor with support for initialization
      and configuraiton from command line args: `ExecController.from_args()`

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

    ExecController is extended by ApiController
    """

    # fmt: off
    __slots__ = ("config", "executor", "main_loop",
                 "loop_policy", "managed_loops",
                 "task_group", "exit_future",
                 "logger",)
    # fmt: on

    config: Configuration
    """Configuration for this controller

    This Configuration object will be initialized within the
    generalized constructor, `ExecController.from_args()`
    """

    executor: ThreadPoolExecutor
    """Thread pool executor for this controller

    The executor will be defined as the default executor for the
    controller's main loop.

    This executor is available mainly via `ExecController.dispatch()`
    """

    main_loop: aio.AbstractEventLoop
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
    exec controller, an event loop policy can be specified
    in Configuration
    """

    managed_loops: SimpleQueue[aio.AbstractEventLoop]
    """Event loops managed with this controller

    As representing a stateful queue, this value should
    generally not be modified external to the controller.
    """

    task_group: aio.TaskGroup
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

    logger: logging.Logger

    app_name: ClassVar[str]
    appdirs: ClassVar[AppDirs]

    @classmethod
    def get_default_config_file(cls):
        return os.path.join(cls.appdirs.user_config_dir, "config.ini")

    @classmethod
    def __init_subclass__(cls, *args, **kw):
        super(*args, **kw)
        if not hasattr(cls, "app_name"):
            try:
                cls.app_name = find_distribution(cls.__module__).name
            except PackageNotFoundError:
                cls.app_name = cls.__name__
        if not hasattr(cls, "appdirs"):
            cls.appdirs = AppDirs(appname=cls.app_name, multipath=True, roaming=True)

    @classmethod
    @contextmanager
    def argparser(
        cls, prog: Optional[str] = None, description: Optional[str] = None
    ) -> Iterator[ap.ArgumentParser]:
        assert prog or (
            cls is not ExecController
        ), "argparser() context manager must be called onto a subclass, or `prog` provided"  # nosec B101
        p = prog or cls.app_name

        desc = description or "Run " + str(p)

        ## fairly a broken implementation, this
        with argparser(p, description=desc) as parser:
            # fmt: off
            config_grp = parser.add_argument_group("configuration")
            config_grp.add_argument('-c', "--config", dest="config_file",
                                    default=cls.get_default_config_file(),
                                    help="Load configuration")
            config_grp.add_argument("-d", dest="config_override", metavar=("<option>", "<value>",),
                                    nargs=2, action="append", default=[],
                                    help="Override configuration <option> with <value>")
            # fmt: on
            yield parser

    @abstractmethod
    def process_args(self, namespace: ap.Namespace, unparsed: list[str]):
        raise NotImplementedError(self.process_args)

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
            exc = ThreadPoolExecutor(
                max_workers, "exec_", initializer=self.init_worker_thread
            )
            self.executor = exc
        self.main_loop.set_default_executor(self.executor)
        self.managed_loops = SimpleQueue[aio.AbstractEventLoop]()
        if not hasattr(self, "task_group"):
            self.task_group = aio.TaskGroup()
        if not hasattr(self, "exit_future"):
            self.exit_future = self.main_loop.create_future()
        if not hasattr(self, "logger"):
            self.logger = logger


    @classmethod
    def create_config_file(cls, path: Pathname):
        ## FIXME generalize this to a console app class
        if not os.isatty(sys.stdin.fileno()):
            raise RuntimeError("Unable to create configuration file, interactive input unavailable")
        print()
        print("This application requires a pesonal access token for API requests.")
        print("Access tokens can be created for fxPractice and fxTrade live accounts,")
        print("at the OANDA Hub.")
        print()
        print("To create an access token for an fxPractice account, please visit")
        print("https://www.oanda.com/demo-account/tpa/personal_token")
        print()
        print("This token cannot be retrieved from the Hub, once created.")
        print()
        print("For documentation and instructions for live accounts, please refer to")
        print("https://developer.oanda.com/rest-live-v20/introduction/")
        print()
        try:
            token: str = prompt(
                "Access Token, or keyboard interrupt to cancel: ", is_password=True
            )
        except KeyboardInterrupt:
            print("Exiting", file=sys.stderr)
            sys.exit(1)
        token = token.strip()
        cfg_dir = os.path.dirname(path)
        if not os.path.exists(cfg_dir):
            os.makedirs(cfg_dir)
        with open(path, "a") as stream:
            print("Creating file: " + str(path))
            print("[Configuration]", file=stream)
            stream.write("access_token = ")
            stream.write(token)
            print(file=stream)
        os.chmod(path, stat.S_IWRITE | stat.S_IREAD)

    @classmethod
    def from_args(
        cls, args: list[str],
        config_overrides: Optional[Mapping[str, Any]] = None,
        loop: Union[aio.AbstractEventLoop, Literal[False], None] = None,
    ) -> "ExecController":
        with cls.argparser() as parser:
            parse_args: Collection[str] = ()
            if args == sys.argv:
                parser.prog = args[0]
                parse_args = args[1:]
            else:
                parse_args = args
            # parse args, without activating a cmd func
            options, rest_args = parser.parse_known_args(parse_args)
            cfg_file = options.config_file
            cfg_path = expand_path(cfg_file)
            if not os.path.exists(cfg_path):
                # initialize a configuration file
                print("Configuration not found: %s" % cfg_file) ## FIXME log info
                cls.create_config_file(cfg_path)
            ## initialize the exec controller
            ##
            ## order of precedence for config overrides:
            ## - if cmdline overrides are provided via the parsed args,
            ##   those will override any values in 'overrides' and any
            ##   defaults in the config
            ##
            ## - any values in a truthy 'overrides' arg will override
            ##   any config options, excepting those overriden from
            ##   cmdline args
            ##
            ## - defaults will be applied from the Configuration class,
            ##   when applicable
            ##
            ## The auth_token arg must be specified in at least one of:
            ##
            ## - the configuration file. This file may have been
            ##   newly created with the required auth token, under
            ##   cls.create_config_file()
            ##
            ## - the 'overrides' arg, for instance if the auth token was
            ##   initialized outside of the configuration file
            ##  (e.g empty exec_token in the config file, loading the actual
            ##   token from a keyring)
            ##
            ## - cmdline arg '-d exec_token <token>' arg, this being the
            ##   least secure possible approach
            inst: ExecController = cls.__new__(cls)
            over = dict(config_overrides) if config_overrides else dict()
            opt_overrides = options.config_override
            if len(opt_overrides) is not int(0):
                over.update(dict(opt_overrides))
            config = load_config(cfg_file, over)
            inst.config = config

            policy_cb = config.__class__.get_callable(config.event_loop_policy)
            policy = policy_cb()
            main_loop = None
            if loop:
                main_loop = loop
            elif loop is False:
                main_loop = policy.get_event_loop()
            else:
                try:
                    main_loop = aio.get_running_loop()
                except:
                    main_loop = policy.get_event_loop()
            inst.loop_policy = policy
            inst.main_loop = main_loop  # type: ignore
            exec_cb = config.__class__.get_callable(config.executor)
            # Pre-initialize the executor, given cmdline args and config
            # Caveat: The executor callback must accept the following args
            inst.executor = exec_cb(max_workers = config.max_thread_workers,
                                    thread_name_prefix = "exec_",
                                    initializer=inst.init_worker_thread)
            inst.initialize_defaults()
            inst.process_args(options, rest_args)
            return inst


    def log_repr(self):
        return "<%s at 0x%x>" % (
            self.__class__.__name__,
            id(self),
        )

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
            async with self.exit_future:
                pass
        except:  # nosec B110
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

        An example implementation is avaialble for the ApiController
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
        """
        try:
            yield self
            return self.main_loop.run_until_complete(self.run_trampoline())
        except:
            # fmt:" off
            etyp, exc, tbk = sys.exc_info()
            self.present_exception(etyp, exc, tbk,
                                   msg="Error under run_context for %s",
                                   msg_args=(self.log_repr(),))
            # fmt: on
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

    def get_future_callback(
        self, call_to: Callable[..., Awaitable], *args, **kwargs
    ) -> Callable[[aio.Future], Any]:
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

    def present_exception(
        self, etype=None, exception=None, tbk=None, msg="Error", msg_args=()
    ):
        # fmt: off
        self.logger.critical(msg, *msg_args,
                             exc_info=(etype, exception, tbk,))
        # fmt: on

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
            except:
                # fmt: off
                etyp, exc, tbk = sys.exc_info()
                self.present_exception(etyp, exc, tbk,
                                       msg="Errors in task_context for %s",
                                       msg_args=(self.log_repr(),))
                # fmt: on
            finally:
                thread_loop.set(loop_pre)


__all__ = ("thread_loop", "ExecController")
