"""ExecController definition"""


from abc import ABC, abstractmethod
from appdirs import AppDirs
import atexit
import argparse as ap
import asyncio as aio
import atexit
from concurrent.futures import CancelledError
from contextlib import contextmanager, asynccontextmanager, suppress
from contextvars import ContextVar
from itertools import chain
import logging
import logging.config
import os
import platform
from quattro import TaskGroup
import signal
import stat
import threading
if platform.system != "Windows":
    import uvloop

from concurrent.futures import ThreadPoolExecutor # TBD blocking in atexit per assumptions in the design of it
import concurrent.futures as cofutures
from functools import partial
from prompt_toolkit import prompt
from queue import SimpleQueue
import sys
import time
from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Collection,
    Coroutine,
    Iterator,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Union,
    TYPE_CHECKING
)
from typing_extensions import ClassVar, Self, TypeVar

from .util.dist import class_distribution, module_dir, PackageNotFoundError
from .util.args import argparser
from .util.log import log_formatter, console_handler, configure_logger
from .util.aio import chain_cancel_callback, safe_running_loop
from .util.cofuture import CoFuture, CoFuturePool
from .util.paths import Pathname, expand_path

from .configuration import Configuration
from .config_manager import load_config


T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)

logger: logging.Logger = logging.getLogger(__name__)

thread_loop: ContextVar[aio.AbstractEventLoop] = ContextVar("thread_loop")
"""
Context Variable storage for a primary event loop

Within `ExecController.async_context()` this context variable will
be bound to the controller's primary event loop.

Within threads created under `ExecController.dispatch()` this
context variable will be bound to an event loop initialized
for the thread.

See also:
- ExecController.dispatch()
- ExecController.async_context() [context manager]
"""


# https://zopeinterface.readthedocs.io/en/latest/README.html#defining-interfaces
# ...


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

    task_group: TaskGroup
    """Task group for this controller.

    Coroutines may be added to this task group with the controller
    method, `add_task()`
    """

    exit_future: CoFuturePool
    """The exit future for this controller.

    This future will be applied to ensure that any context manager onto
    the exec controller's task group will not return until this future
    has been set to a 'done' state. This is managed mainly via the
    methods, `run_trampoline()` and `await_exit()`, such that would
    be called via the synchronous `run_context()` context manager
    when dispatching to `run_async()` for the implementing class.
    """

    logger: logging.Logger
    """Logger for this controller"""

    exceptions: set[Exception]
    """Exceptions received by present_exception()"""

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
                cls.app_name = class_distribution(cls).name
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
            net_grp = parser.add_argument_group("network")
            net_grp.add_argument("--no-proxy", dest="no_proxy",
                                    action="store_true", default=False,
                                    help="Disable proxy support")
            config_grp = parser.add_argument_group("configuration")
            config_grp.add_argument('-c', "--config", dest="config_file",
                                    default=cls.get_default_config_file(),
                                    help="Load configuration")
            config_grp.add_argument("-D", "--config-override", dest="config_override", metavar=("<option>", "<value>",),
                                    nargs=2, action="append", default=[],
                                    help="Override configuration <option> with <value>, e.g -D timestamp_format '<strftime...>'")
            config_grp.add_argument("-L", "--log-level", dest="log_levels", metavar=("<logger>", "<level>",),
                                    nargs=2, action="append", default=[],
                                    help="Set log <level> for <logger>, 'root' or empty string '' for root logger")
            config_grp.add_argument("--log-config", dest="log_config_file", metavar="ini_file",
                                    default=None,
                                    help="Load custom logger configuration")
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
        try:
            if self.exit_future.done():
                raise RuntimeError("init_worker_thread while exiting", self)
            aio.set_event_loop_policy(self.loop_policy)
            loop = self.loop_policy.new_event_loop()
            aio.set_event_loop(loop)
            thread_loop.set(loop)
            self.managed_loops.put(loop)
        except Exception:
            self.present_exception(sys.exc_info(), msg="Exception when initializing thread")

            raise

    def initialize_defaults(self):
        """
        Initialize all default properties for this controller

        - Called after configuration has been initialized for
          the instance

        - Initialize the controller's thread pool executor,
          using the  `max_thread_workers` property selected
          in this controller's configuration.

        - Initialize an internal loop management queue, for
          reference to the primary asyncio loop in each
          worker thread

        The executor will be created with an initializer
        calling `init_worker_thread()` for this controller.

        ### Known Limitations

        The worker loop management queue is initialized with
        an asumption that this controller's `close()` function will
        be called within at most one thread.
        """
        global logger
        config = self.config
        max_workers = config.max_thread_workers
        if not hasattr(self, "executor"):
            exec_cb = config.__class__.get_callable(config.executor)
            exc = exec_cb(
                max_workers=max_workers,
                thread_name_prefix="exec_",
                initializer=self.init_worker_thread
            )
            self.executor = exc

        ## main_loop is initialized typically under from_args ...
        self.main_loop.set_default_executor(self.executor)

        self.managed_loops = SimpleQueue()
        if not hasattr(self, "task_group"):
            self.task_group = TaskGroup()
        if not hasattr(self, "exit_future"):
            self.exit_future = CoFuturePool("main", result_value=0)
        if not hasattr(self, "logger"):
            ## the controller's logger is used under present_exception()
            self.logger = logging.getLogger(self.app_name)
        if not hasattr(self, "exceptions"):
            self.exceptions = set()

    @classmethod
    def get_log_formatter(cls) -> logging.Formatter:
        """Return a log formatter for use with `configure_loggers()`

        This method may be overridden or extended, in extending classes
        """
        return log_formatter()

    @classmethod
    def get_log_handlers(cls) -> list[logging.Handler]:
        """Return a console log handler for use with `configure_loggers()`

        The console handler - as a log stream handler - will produce
        logging output to `sys.stderr`, using a formatter initialized by
        `cls.get_log_formatter()`

        This method may be overridden or extended, in extending classes
        """
        formatter = cls.get_log_formatter()
        return [console_handler(stream=sys.stderr, formatter=formatter)]

    @classmethod
    def configure_loggers(cls):
        """
        Configure loggers for this controller

        This method on ExecController will initialize the root logger,
        using log handlers initialized with `cls.get_log_handlers()`.

        The default log handlers list will include a stream handler
        producing log output to `sys.stderr`, with a formatter
        initialized to provide process ID, timestamp, thread ID,
        logger, and log message information. This handlers list will
        be applied to extend the set of existing root log handlers.

        This method may be overridden or extended, in extending classes.

        ### Implementation Note: Logging configuration in `from_args()`

        When the args list provided to `from_args()` has specified
        a logging config  file, the logging configuration in that
        file will be applied as  instead of calling `configure_loggers()`.
        Additional loggers can be initialized per instance, such as
        within a `process_args()` method defined in an extending class,
        or as previous to calling the class method, `from_args()`.

        Independent to the configuration for log formatting and
        log process handling, logging level may be set for
        individual loggers, using args provided to `from_args()`.

        The exact args syntax for `from_args()` may generally be
        determined by calling the respective `__main__` module
        with the arg `--help`
        """
        handlers = cls.get_log_handlers()
        configure_logger(handlers=handlers)

    @classmethod
    def create_config_file(cls, path: Pathname):
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
    ) -> Self:
        with cls.argparser() as parser:
            parse_args: Collection[str] = ()

            if args == sys.argv:
                parser.prog = os.path.basename(args[0])
                parse_args = args[1:]
            else:
                parse_args = args

            # parse args, without activating a cmd func
            options, rest_args = parser.parse_known_args(parse_args)

            #
            # initialize loggers
            #
            log_cfg: Optional[Pathname] = options.log_config_file
            if log_cfg:
                try:
                    logging.config.fileConfig(log_cfg)
                except:
                    logger.critical("Unable to parse log config file %r", log_cfg, exc_info=sys.exc_info())
                    logger.critical("Using default log config")
                    cls.configure_loggers()
            else:
                cls.configure_loggers()

            logging_ns = logging.__dict__
            for logname, level in options.log_levels:
                if TYPE_CHECKING:
                    logname: str
                    level: str
                try:
                    use_level = int(level)
                except ValueError:
                    use_level = logging_ns.get(level.upper(), None)

                if use_level and isinstance(use_level, int):
                    named = logging.getLogger(logname)
                    named.setLevel(use_level)
                else:
                    logger.critical("Unknown log level %r", level)

            #
            # parse config
            #
            cfg_file = options.config_file
            logger.info("Using config file %s", cfg_file)
            cfg_path = expand_path(cfg_file)
            if not os.path.exists(cfg_path):
                # initialize a configuration file
                print("Configuration not found: %s" % cfg_file)
                cls.create_config_file(cfg_path)

            ##

            inst: ExecController = cls.__new__(cls)
            over = dict(config_overrides) if config_overrides else dict()
            opt_overrides = options.config_override
            if len(opt_overrides) is not int(0):
                over.update(dict(opt_overrides))
            config_fields = Configuration.model_fields
            over_na = []
            for name in over.keys():
                if name not in config_fields:
                    logger.critical("cli: Unknown configuration field: %s", name)
                    over_na.append(name)
            for name in over_na:
                del over[name]
            config = load_config(cfg_file, over)
            inst.config = config

            if options.no_proxy:
                config.proxy = None

            if loop:
                main_loop = loop
            else:
                running_loop = None
                with suppress(RuntimeError):
                    running_loop = aio.get_running_loop()
                if running_loop is not None:
                    ## e.g running under IPython, Jupyter, ...
                    ##
                    ## skipping the configured event loop policy here
                    main_loop = running_loop
                else:
                    policy_cb = config.__class__.get_callable(config.event_loop_policy)
                    policy: aio.AbstractEventLoopPolicy = policy_cb()
                    if platform.system != "Windows" and isinstance(policy, uvloop.EventLoopPolicy):
                        uvloop.install()

                    inst.loop_policy = policy
                    aio.set_event_loop_policy(policy)

                    try:
                        main_loop = policy.get_event_loop()
                    except RuntimeError:
                        main_loop = policy.new_event_loop()

            inst.main_loop = main_loop  # type: ignore

            exec_cb = config.__class__.get_callable(config.executor)
            # Pre-initialize the executor, given cmdline args and config
            # Caveat: The executor callback must accept the following args
            inst.executor = exec_cb(max_workers=config.max_thread_workers,
                                    thread_name_prefix="exec_",
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

        It's assumed that this coroutine will be called within the same
        thread and event loop as where the controller's `exit_future` was
        initialized, such as typically within the controller's `main_loop`.
        """
        try:
            await self.exit_future.apoll()
        except:  # nosec B110
            pass

    def dispatch(self, func: Callable[..., T], *args, **kwargs) -> aio.Future[T]:
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
            return self.main_loop.run_in_executor(self.executor, func, *args)
        else:
            call = partial(func, *args, **kwargs)
            return self.main_loop.run_in_executor(self.executor, call)

    def close(self, immediate: bool = False):
        """
        Close this controller

        `close()` will perform the following generalized procedure:

        1. Cancel all unfinished tasks under each worker loop,
        also capturing and logging any task exceptions

        2. Close each worker loop

        3. Pause asynchronously for `sys.getswitchinterval()` seconds
        before return, to allow for normal exit under cancelled tasks
        """
        delay = None if immediate else sys.getswitchinterval()
        self.exit_future.close()
        if delay:
            time.sleep(delay)
        loop_queue = self.managed_loops
        ## close worker loops
        if __debug__:
            logger.debug("closing worker loops")
        while not loop_queue.empty():
            worker_loop = loop_queue.get()
            try:
                for task in aio.all_tasks(worker_loop):
                    task.cancel()
            finally:
                worker_loop.stop()
                if delay:
                    time.sleep(delay)
                with suppress(RuntimeError):
                    worker_loop.close()
        if delay:
            time.sleep(delay)
        ## close worker threads
        if __debug__:
            logger.debug("closing executor")
        # cofutures.thread._threads_queues.clear()
        self.executor.shutdown(wait=False, cancel_futures=True)

    def exit(self, code: Optional[int] = 0, immediate: bool = False):
        logger.critical("Exiting: %r (%r)", code, immediate)
        self.close(immediate)
        sys.exit(code)

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
        an asynchronous `async_context()` for the ExecController.

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
        async with self.async_context():
            with suppress(cofutures.CancelledError, aio.CancelledError):
                try:
                    return await self.run_async()
                finally:
                    if __debug__:
                        logger.debug("run_trampoline: await exit_future")
                    await self.exit_future
                    if __debug__:
                        logger.debug("run_trampoline: return")

    @contextmanager
    def run_context(self) -> Iterator[Self]:
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
        initial_sigint_handler = None
        own_loop = True
        try:
            atexit.register(self.close, True)
            with suppress(ValueError):
                initial_sigint_handler = signal.signal(signal.SIGINT, lambda *_: self.exit_future.cancel())
            yield self
            loop = self.main_loop
            own_loop = not loop.is_running()
            running_loop = None
            with suppress(RuntimeError):
                ## poratbility for ipython
                running_loop = aio.get_running_loop()
            if own_loop and running_loop is None:
                _ = self.main_loop.run_until_complete(self.run_trampoline())
            elif running_loop:
                raise RuntimeError("Found a running event loop. %s must be run under a separate thread" % self.__class__.__name__)
            else:
                ## could be reached if the main_loop is already running
                raise RuntimeError("%s unable to run event loop" % self.__class__.__name__)
        except:
            # fmt:" off
            self.present_exception(*sys.exc_info(),
                                   msg="Error under run_context for %s",
                                   msg_args=(self.log_repr(),))
            raise
            # fmt: on
        finally:
            if initial_sigint_handler:
                signal.signal(signal.SIGINT, initial_sigint_handler)
            self.close()
            if own_loop:
                if __debug__:
                    logger.debug("closing main loop")
                loop = self.main_loop
                for task in aio.all_tasks(loop):
                    task.cancel()
                loop.stop()
                loop.close()
                if __debug__:
                    logger.debug("main loop closed")

            # return

            interval = sys.getswitchinterval()
            for thread in tuple(threading._active.values()):
                if TYPE_CHECKING:
                    thread: threading.Thread
                with suppress(Exception):
                    thread.join(interval)
            threading._threading_atexits.clear()
            threading._shutdown_locks.clear()

    def add_cofuture(self) -> CoFuture:
        return self.exit_future.create_future()

    def add_task(self, coro: Coroutine[Any, Any, T_co]) -> CoFuture[T_co]:
        """Task inteface for the exec controller's task group

        `add_task()` will create a task calling the provided
        coroutine `coro` within the main loop and main thread
        for this exec controller's task group.

        Returns the newly created task
        """
        try:
            running = False
            with suppress(RuntimeError):
                running = aio.get_running_loop()
            main = self.main_loop
            coro_future = None
            if running is main:
                # here :: coro_future: aio.Task
                coro_future = self.task_group.create_task(coro)
                chain_cancel_callback(self.exit_future, coro_future)
            else:
                # here :: coro_future: concurrent.futures.Future
                coro_future = aio.run_coroutine_threadsafe(coro, main)
            #
            # returning a uniform thread-safe, awaitable CoFuture interface
            # for the task or concurrent future
            #
            cofuture = self.add_cofuture("add_task_" + hex(id(coro)))
            def pass_result(cfaio: CoFuture, future: aio.Future): ## rly AnyFuture
                if future.cancelled():
                    cfaio.cancel()
                    return
                exc = future.exception()
                if exc:
                    cfaio.set_exception(exc)
                    return
                with suppress(cofutures.InvalidStateError, cofutures.CancelledError):
                    cfaio.set_result(future.result())
            coro_future.add_done_callback(partial(pass_result, cofuture))
            chain_cancel_callback(self.exit_future, coro_future)
            return cofuture
        except Exception as exc:
            logger.critical("Failed to start task %r : %r", coro, exc)
            raise

    def add_cofuture(self, name: Optional[str] = None, **kw) -> CoFuture:
        return self.exit_future.create_future(name, **kw)

    def get_future_callback(
        self, call_to: Callable[..., Coroutine], *args, **kwargs
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
        exc = exception or etype
        if exc not in self.exceptions:
            # fmt: off
            self.logger.critical(msg, *msg_args,
                                exc_info=(etype, exception, tbk,))
            # fmt: on
            self.exceptions.add(exc)

    @asynccontextmanager
    async def async_context(self) -> AsyncIterator[TaskGroup]:
        """Async context manager for ExecController.task_group handling

        ## Usage

        This context manager is applied under ExecController.run_trampoline()

        ## Synopsis

        - Bind the current thread's `thread_loop` context variable to
        the main loop for this controller, within the calling context

        - Await all tasks within the ExecController's task group, before
        return
        """
        async with self.task_group as tg:
            loop_pre = thread_loop.set(self.main_loop)
            try:
                yield tg
            finally:
                thread_loop.reset(loop_pre)
                if hasattr(tg, "_tasks"):
                    for task in tg._tasks:
                        task.cancel()

    def main(self) -> int:
        with self.exit_future:
            with self.run_context():
                if __debug__:
                    term_program = os.getenv("TERM_PROGRAM", None)
                    if term_program == "vscode" and "debugpy" in sys.modules:
                        #
                        # load additional debugger support for multi-
                        # threaded applications in VS Code
                        # https://stackoverflow.com/a/3242780/1061095
                        #
                        try:
                            import pydevd  # type: ignore[import-untyped]
                            pydevd.connected = True
                            pydevd.settrace(suspend=False)
                        except:
                            logger.warning("Failed to initialize pydevd", exc_info=sys.exc_info())
        try:
            result = self.exit_future.result(0)
            return result if isinstance(result, int) else 1
        except:
            return 1

    @classmethod
    def run_threaded(cls, additional_args: Optional[Sequence[str]] = None) -> tuple[Self, threading.Thread]:
        import traceback
        try:
            def run(cls: Self, args, future: CoFuture):
                with future:
                    try:
                        if __debug__:
                            logger.debug("Initializing controller")
                        controller = cls.from_args(args)
                        future.set_result(controller)
                        if __debug__:
                            logger.debug("Main: %r", controller)
                        controller.main()
                    except SystemExit:
                        # reached e.g when args includes "--help"
                        if __debug__:
                            logger.debug("Controller initialization cancelled")
                        future.cancel()
                    except Exception as exc:
                        logger.critical("Error initializing controller", exc_info=sys.exc_info())
                        with suppress(cofutures.InvalidStateError, cofutures.CancelledError):
                            future.set_exception(exc)
            inst_future = CoFuture(cls.__name__ + "::run")
            import threading
            thread = threading.Thread(target=run, args=(cls, additional_args or (), inst_future,), daemon=True)
            if __debug__:
                logger.debug("Running %s under new thread 0x%x", cls.__name__, thread.native_id or 0)
            thread.start()
            try:
                controller = inst_future.poll()
            except cofutures.CancelledError as exc:
                raise RuntimeError("Controller initialization cancelled") from exc
            return controller, thread
        except:
            info = sys.exc_info()
            traceback.print_exception(*info, file=sys.stderr)
            logger.critical("%s.run_threaded: Exiting", cls.__name__, exc_info=info)
            raise

    @classmethod
    def run_main(cls, additional_args: Optional[Sequence[str]] = None):
        running_loop = safe_running_loop()
        main_args = [] if additional_args is None else list(additional_args)
        if running_loop is None:
            #
            # using sys.argv and any additional args
            #
            if __debug__:
                logger.debug("Running %s under current thread", cls.__name__)
            return cls.from_args(sys.argv + main_args).main()
        else:
            #
            # discarding sys.argv when running in a thread
            # beside an existing event loop
            #
            cls.run_threaded(additional_args)
__all__ = ("thread_loop", "ExecController")
