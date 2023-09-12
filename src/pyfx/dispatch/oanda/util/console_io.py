## Asynchronous Console I/O Support with aioconsole

import aioconsole
import asyncio as aio
from contextlib import asynccontextmanager
import sys
from typing_extensions import TypeAlias, Optional, Union


ConsoleStreamReader: TypeAlias = Union[aioconsole.stream.StandardStreamReader, aioconsole.stream.NonFileStreamReader]
ConsoleStreamWriter: TypeAlias = Union[aioconsole.stream.StandardStreamWriter, aioconsole.stream.NonFileStreamWriter]


class ConsoleIO:
    def __init__(self, loop: aio.AbstractEventLoop,
                 reader: aio.StreamReader,
                 out_writer: aio.StreamWriter,
                 err_writer: Optional[aio.StreamWriter]):
        self._loop = loop
        self._reader = reader
        self._out_writer = out_writer
        self._err_writer = err_writer if err_writer else out_writer

    @property
    def stdin_reader(self) -> ConsoleStreamReader:
        return self._reader

    @property
    def stdout_writer(self) -> ConsoleStreamWriter:
        return self._out_writer

    @property
    def stderr_writer(self) -> ConsoleStreamWriter:
        return self._err_writer

    async def close(self):
        ## drain and close the writer streams
        self.stdout_writer.close()
        await self.stdout_writer.wait_closed()
        self.stderr_writer.close()
        await self.stderr_writer.wait_closed()


@asynccontextmanager
async def console_io(stderr_out: bool = False, loop: Optional[aio.AbstractEventLoop] = None):
    ## async context manager shim
    pipe = None
    stdout = sys.stdout
    stderr = sys.stderr
    stdin = sys.stdin
    try:
        aio_loop = loop if loop else aio.get_running_loop()
        s_in, s_out, s_err = await aioconsole.stream.create_standard_streams(sys.stdin, sys.stdout, sys.stderr, loop=aio_loop)
        pipe = ConsoleIO(loop, s_in, s_out, s_err)
        sys.stderr = pipe.stderr_writer
        sys.stdout = pipe.stdout_writer
        sys.stdin = pipe.stdin_reader
        yield pipe
    finally:
        sys.stder = stderr
        sys.stdout = stdout
        sys.stdin = stdin
        if pipe:
            await pipe.close()
