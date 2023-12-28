"""Asynchronous Console I/O Support with aioconsole"""

import aioconsole
import atexit
import asyncio as aio
from contextlib import asynccontextmanager, suppress
import os
from quattro import move_on_after
import sys
import traceback
from typing_extensions import TypeAlias, Optional, Union

from .naming import exporting

ConsoleStreamReader: TypeAlias = Union[aioconsole.stream.StandardStreamReader, aioconsole.stream.NonFileStreamReader]
ConsoleStreamWriter: TypeAlias = Union[aioconsole.stream.StandardStreamWriter, aioconsole.stream.NonFileStreamWriter]


class ConsoleIO:
    '''Streams wrapper for aioconsole via console_io()'''
    def __init__(self, loop: aio.AbstractEventLoop,
                 reader: aio.StreamReader,
                 out_writer: aio.StreamWriter,
                 err_writer: Optional[aio.StreamWriter]):
        self._loop = loop
        self._reader = reader
        self._out_writer = out_writer
        self._err_writer = err_writer if err_writer else out_writer

    __slots__ = ("_loop", "_reader", "_out_writer", "_err_writer")

    @property
    def stdin_reader(self) -> ConsoleStreamReader:
        return self._reader

    @property
    def stdout_writer(self) -> ConsoleStreamWriter:
        return self._out_writer

    @property
    def stderr_writer(self) -> ConsoleStreamWriter:
        return self._err_writer

    def close(self):
        ## close stdout, stderr writers without flush
        stdout = self.stdout_writer
        stdout.close()
        stderr = self.stderr_writer
        if stderr is not stdout:
            stderr.close()

    async def aclose(self):
        stdout = self.stdout_writer
        stdout.close()
        try:
            await stdout.wait_closed()
        except:  # nosec B110
            pass
        stderr = self.stderr_writer
        if stderr is not stdout:
            stderr.close()
            try:
                await stderr.wait_closed()
            except:  # nosec B110
                pass


@asynccontextmanager
async def console_io(*, stderr_out: bool = False, loop: Optional[aio.AbstractEventLoop] = None):
    '''Async context manager for aioconsole streams

    On entry to the context manager, creates a new ConsoleIO object for sys.stdin, sys.stdout,
    and sys.stderr. A new ConsoleIO object will be returned the caller, containing each of
    these asynchronous streams.

    The new streams are created with `aioconsole.stream.create_standard_streams()`

    Within the context scope of the context manager, each of the `sys` streams is replaced
    with the corresopnding aioconsole stream.

    On exit from the context manager, the stdout, stderr, and stdin streams are each set to
    the stream that was acvtive when the context manager was entered, then the ConsoleIO
    object is closed. By side effect, this will drain and close the asynchronous output
    streams.

    Known Limitations:

    - Provided as a utilty for general applications in console scripts, this context
      manager may not serve as a complete asyncio replacement for the operating system's
      PTY implementation, or for any PTY-like interface for the host system.

    - asyncio streams are each managed under the asyncio event loop for the primary thread.
      As such, this context manager may produce any undetermined side effects on event of
      error, and on event of unexpected loop closure.

      For instance, with Python on Microsoft Windows platforms, messages such as "Lost stdout"
      may appear during a bracktrace, in an application of this context manager.

      Output from Python Debug mode is not known to be adversely affected with this feature.
    '''
    pipe = None
    stdout = sys.stdout
    stdout_fd = os.dup(stdout.fileno())
    stderr = sys.stderr
    stderr_fd = None if stderr is stdout else os.dup(stderr.fileno())
    stdin = sys.stdin
    stdin_fd = os.dup(stdin.fileno())
    try:
        aio_loop = loop or aio.get_running_loop()
        s_in, s_out, s_err = await aioconsole.stream.create_standard_streams(sys.stdin, sys.stdout, sys.stderr, loop=aio_loop)
        pipe = ConsoleIO(loop, s_in, s_out, s_err)
        sys.stderr = pipe.stderr_writer
        sys.stdout = pipe.stdout_writer
        sys.stdin = pipe.stdin_reader
        yield pipe
    finally:
        # Open a fallback stream for each original file descriptor
        #
        # This should serve to ensure normal I/O is available before sys.exit()
        #
        # Known Limitations:
        #
        # It's assumed that the original sys streams are each bound to some object
        # having a fileno(), furthermore assumed that the dup'd file descriptors
        # are each accepting I/O at this time
        #
        # Not a complete stream dup-lication, this does not restore buffering or other
        # properties of the original streams
        #
        sys.stdout = open(stdout_fd, encoding=stdout.encoding, mode=stdout.mode)
        atexit.register(sys.stdout.close)
        if stderr_fd:
            sys.stderr = open(stderr_fd, encoding=stderr.encoding, mode=stderr.mode)
            atexit.register(sys.stderr.close)
        else:
            sys.stderr = sys.stdout

        sys.stdin = open(stdin_fd, encoding=stdin.encoding, mode=stdin.mode)
        atexit.register(sys.stdin.close)
        if pipe:
            try:
                with move_on_after(sys.getswitchinterval()):
                    await pipe.aclose()
            except:
                print("Error during ConsoleIO.aclose()", file=stderr)
                traceback.print_exception(*sys.exc_info(), file=stderr)
            finally:
                pipe.close()


__all__ = exporting(__name__, ..., annotations=True)
