

from contextvars import ContextVar
from .configuration import Configuration
from .config_manager import load_config
import asyncio as aio
import os
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from functools import partial
from queue import SimpleQueue
import sys
import time
from typing import Callable, Optional, Self
from typing_extensions import TypeVar

T = TypeVar("T")


__all__ = ("thread_loop", "ExecController")

thread_loop: ContextVar[aio.AbstractEventLoop] = ContextVar('thread_loop')


@dataclass(eq=False, order=False)
class ExecController():
    ## base class for DispatchController, without API class dependencies
    config: Configuration
    executor: ThreadPoolExecutor = field(hash=False)
    main_loop: aio.AbstractEventLoop = field(hash=False)
    loop_policy: aio.AbstractEventLoopPolicy

    managed_loops: SimpleQueue[aio.AbstractEventLoop]

    def init_worker_thread(self, policy: aio.AbstractEventLoopPolicy):
        ## create an asyncio event loop for the thread, setting that
        ## loop as the thread's loop and setting the thread's
        ## thread_loop context value to that loop.
        ##
        ## The loop should then be consistently available for async
        ## callbacks dispatched within the thread - mainly via
        ## thread_loop.get()
        ##
        ## FIXME on supported platforms, use a uvloop here
        try:
            loop = policy.new_event_loop()
            aio.set_event_loop(loop)
            thread_loop.set(loop)
            self.managed_loops.put(loop)
            if __debug__:
                loop.set_debug(sys.platform == "win32")
        except Exception as exc:
            print(exc)
            raise

    def initialize_defaults(self):
        max_workers = self.config.max_read_workers
        exc = ThreadPoolExecutor(max_workers, "exec_",
                                 initializer=self.init_worker_thread,
                                 initargs=(self.loop_policy,))
        self.main_loop.set_default_executor(exc)
        self.executor = exc
        self.managed_loops = SimpleQueue[aio.AbstractEventLoop]()

    @classmethod
    def from_config_ini(cls, path: os.PathLike = "account.ini",
                        loop: Optional[aio.AbstractEventLoop] = None,
                        loop_policy: Optional[aio.AbstractEventLoopPolicy] = None
                        ) -> Self:
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

    ## dispatch a synchronous callable to the executor for this controller
    ##
    ## the callable may dispatch to the thread's event loop, internally
    async def dispatch(self, func: Callable[..., T], *args, **kwargs) -> T:
        if len(kwargs) is int(0):
            return await self.main_loop.run_in_executor(self.executor, func, *args)
        else:
            call = partial(func, *args, **kwargs)
            return await self.main_loop.run_in_executor(self.executor, call)

    def close(self):
        self.main_loop.run_until_complete(self.api_client.rest_client.aclose())
        q = self.managed_loops
        while not q.empty():
            loop = q.get()
            # print("Closing "+ repr(loop))
            for task in aio.all_tasks(loop):
                task.cancel()
                exc = task.exception()
                if exc:
                    ## TBD additional exception handling at the controller scope
                    # print("EXC in ..." + pformat(exc))
                    print(exc)
            loop.close()
        time.sleep(sys.getswitchinterval())

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
