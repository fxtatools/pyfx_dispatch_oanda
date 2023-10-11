from abc import abstractmethod
import asyncio as aio
import math
import concurrent.futures
import os
import sys
import time
from queue import SimpleQueue
from typing import Generic, Optional
from typing_extensions import Generic, Protocol, TypeVar

from enum import IntEnum

Tdata = TypeVar("Tdata", bound="SequenceLike")


class SequenceLike(Protocol, Generic[Tdata]):
    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError(self.__len__)

    @abstractmethod
    def __getitem__(self, key) -> Tdata:
        raise NotImplementedError(self.__getitem__)


class IoState(IntEnum):
    NoState = 0
    Closed = 1


class DataError(Exception):
    pass


class EndOfFile(DataError):
    pass


class ClosedError(DataError):
    pass


class Segment(Generic[Tdata]):
    ## partial implementation for segmented read()

    __slots__ = ("_data", "_len", "_cursor", "_last", "_eof")

    @property
    def data(self) -> Tdata:
        return self._data

    @property
    def len(self) -> int:
        return self._len

    @property
    def cursor(self) -> int:
        return self._cursor

    @property
    def eof(self) -> bool:
        return self._eof

    def __init__(self, data: Tdata, eof: bool = False):
        self._data = data
        self._len = len(data)
        self._eof = eof
        self._cursor = 0

    def read(self, n: int = -1) -> Tdata:
        data = self.data
        last = self.len
        if n is int(-1) or n is math.inf:
            rslt = data[self.cursor:]
            self._cursor = last
            return rslt
        else:
            cursor = self._cursor
            end = cursor + n
            if end > last:
                raise aio.IncompleteReadError(expected=n, partial=data[cursor:last])
            else:
                rslt = data[self.cursor:end]
                self._cursor = end
                return rslt

class SegmentChannel(Generic[Tdata]):
    ## Synchronous SegmentChannel / common base class

    ## This implementation allows for feed() of arbitrary bytes or
    ## strings, with a stream-like read() function available ofor
    ## parsing the effective concatenation of the input values
    ##
    ## Assumption: All input values will beof the same type

    __slots__ = ("_read_queue", "_closed_future", "_eof",
                 "_empty_sequence", "_line_separator",
                 "_current_segment", "_poll_interval")


    @property
    def eof(self) -> bool:
        return self._eof

    @eof.setter
    def eof(self, value: bool):
        self._eof = value

    @property
    def empty_sequence(self) -> Tdata:
        return self._empty_sequence

    @empty_sequence.setter
    def empty_sequence(self, value: Tdata):
        self._empty_sequence = value

    @property
    def line_separator(self) -> Tdata:
        return self._line_separator

    @line_separator.setter
    def line_separator(self, value: Tdata) -> Tdata:
        self._line_separator = value

    @property
    def poll_interval(self) -> int:
        return self._poll_interval

    @property
    def current_segment(self) -> Optional[Segment[Tdata]]:
        return self._current_segment

    @property
    def read_queue(self) -> SimpleQueue[Segment[Tdata]]:
        return self._read_queue

    @property
    def closed_future(self) -> concurrent.futures.Future:
        return self._closed_future


    def __init__(self, empty_sequence: Optional[Tdata] = None,
                 line_separator: Tdata = os.linesep,
                 closed_future: Optional[concurrent.futures.Future] = None):

        self._eof = False
        self._current_segment = None
        self._line_separator = line_separator
        self._poll_interval = sys.getswitchinterval()

        if not hasattr(self, "_read_queue"):
            ## may be overridden in a subclass
            self._read_queue = SimpleQueue[Segment[Tdata]]()

        if closed_future:
            self._closed_future = closed_future
        elif not hasattr(self, "_closed_future"):
            ## default may be overridden in a subclass
            self._closed_future = concurrent.futures.Future()

        if empty_sequence:
            ## if not provided here, empty_sequence will be set with the first
            ## call to feed() such as to use the same sequence type
            ## as the first sequence provided to feed()
            self.empty_sequence = empty_sequence

    def __repr__(self):
        return "<%s [%s] at 0x%x>" % (self.__class__.__name__, self.closed_future, id(self))

    def at_eof(self) -> bool:
        ## this method is defined for the asyncio StreamReader protocol
        return self.eof

    def feed(self, data: Tdata, eof: bool = False):
        if self.eof:
            raise EndOfFile("stream is at EOF")
        elif self.closed():
            raise ClosedError("input queue is closed")
        else:
            if not hasattr(self, "empty_sequence"):
                self.empty_sequence = data[:0]
            self.read_queue.put(Segment(data, eof))

    def feed_line(self, data: Tdata, eof: bool = False):
        return self.feed(data + self.line_separator, eof)

    def next_segment(self) -> Optional[Segment[Tdata]]:
        seg = self._current_segment
        if seg is None:
            if self.closed() or self.eof:
                return None
            else:
                seg = self.read_queue.get()
                self._current_segment = seg
        return seg

    def next_chunk(self) -> Tdata:
        ## usage: provides support for effective read-ahead
        ## returns the next segment data, without advancing cursor
        seg = self.next_segment()
        return seg if seg else self.empty_sequence

    def chunk_done(self):
        self._current_segment = None

    def read(self, n: int = -1) -> Tdata:

        inf = math.inf
        to_read = n if n >= 0 else inf
        have_read = self.empty_sequence
        while to_read >= 0:
            seg = self.next_segment()
            if not seg:
                return have_read
            try:
                # print("Read %s" % to_read)
                seg_read = seg.read(to_read)
                have_read = have_read + seg_read
            except aio.IncompleteReadError as exc:
                partial = exc.partial
                # print("incomplete read %s" % partial)
                have_read = have_read + partial
                self.chunk_done()
                if seg.eof:
                    self.eof = True
                break
            except Exception as exc:
                self.closed_future.set_exception(exc)
                have_read = have_read + partial
                break
            else:
                n_read = len(seg_read)
                # print("Read %d from segment" % n_read)
                if n_read is seg.len:
                    self.chunk_done()
                    seg_eof = seg.eof
                    if seg_eof:
                        self.eof = seg_eof
                if to_read is not inf:
                    to_read = to_read - n_read
                if to_read is int(0):
                    break
        return have_read

    def readline(self) -> Tdata:
        return self.readuntil(self.line_separator)

    def readexactly(self, n: int) -> Tdata:
        assert n >= 0, "n is a negative value"
        rslt = self.read(n)
        if len(rslt) is not int(n):
            raise aio.IncompleteReadError(partial=rslt, expected=n)
        else:
            return rslt

    def readuntil(self, separator: Optional[Tdata] = None) -> Tdata:
        raise NotImplementedError(self.readuntil)

    def aclose(self) -> Optional[aio.Handle]:
        self.eof = True
        future = self.closed_future
        if not future.done():
            future.set_result(IoState.Closed)

    def closed(self):
        return self.closed_future.done()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.aclose()


## The original async implementation - AsyncSegmentChannel

class AsyncSegment(Segment[Tdata]):
    async def read(self, n: int = -1) -> Tdata:
        # synchronous read, with additional call handling
        # via asyncio.
        #
        # In this usage case, the superclass' synchronous
        # read() call is mainly producing a cursor-bounded
        # subsequence onto self.data. The function will not
        # produce any I/O syscalls.
        #
        # The call to await read() in the consuming stream
        # may be accompanied with any additional scheduling
        # support, in the host system's asyncio implementation
        #
        return super().read(n)


class AsyncSegmentChannel(SegmentChannel[Tdata]):

    @property
    def current_segment(self) -> Optional[AsyncSegment[Tdata]]:
        return self._current_segment

    @property
    def read_queue(self) -> SimpleQueue[AsyncSegment[Tdata]]:
        return self._read_queue

    @property
    def closed_future(self) -> aio.Future:
        return self._closed_future

    def __init__(self, empty_sequence: Optional[Tdata] = None,
                 line_separator: Tdata = os.linesep,
                 closed_future: Optional[aio.Future] = None,
                 loop: Optional[aio.AbstractEventLoop] = None):

        if closed_future:
            ## using the provided future for indiating a self.closed() state
            ##
            ## this value is independent to self.eof state
            self._closed_future = closed_future
        else:
            ## initializing a new future, in either the provided loop or in the
            ## effective event loop for the current run context
            self._closed_future = aio.Future(loop=loop if loop else aio.get_event_loop_policy().get_event_loop())

        super().__init__(empty_sequence, line_separator)

    async def feed(self, data: Tdata, eof: bool = False):
        if self.eof:
            raise EndOfFile("stream is at EOF")
        elif self.closed():
            raise ClosedError("input queue is closed")
        else:
            if not hasattr(self, "empty_sequence"):
                self.empty_sequence = data[:0]
            ## Implementation Note:
            ##
            ## This call would not block unless the queue has been replaced
            ## with a bounded queue in some subclass
            self.read_queue.put(AsyncSegment(data, eof))

    async def feed_line(self, data: Tdata, eof: bool = False):
        return await self.feed(data + self.line_separator, eof)

    def feed_sync(self, data: Tdata, eof: bool = False) -> aio.Task:
        loop = self.closed_future.get_loop()
        return loop.run_until_complete(self.feed(data, eof))

    def feed_line_sync(self, data: Tdata, eof: bool = False) -> aio.Task:
        loop = self.closed_future.get_loop()
        return loop.run_until_complete(self.feed_line(data, eof))

    def read_sync(self, n: int = -1) -> Optional[Tdata]:
        loop = self.closed_future.get_loop()
        return loop.run_until_complete(self.read(n))

    async def read(self, n: int = -1) -> Tdata:
        inf = math.inf
        to_read = n if n >= 0 else inf
        sleep_for = self.poll_interval
        have_read = self.empty_sequence if hasattr(self, "empty_sequence") else None
        while to_read >= 0:
            queue = self.read_queue
            seg = self._current_segment
            if seg == None:
                # print("Fetch next segment")
                if self.closed() or self.eof:
                    return have_read
                seg = queue.get()
                self._current_segment = seg
            try:
                # print("Read %s" % to_read)
                seg_read = await seg.read(to_read)  # x async
                have_read = have_read + seg_read
            except aio.IncompleteReadError as exc:
                partial = exc.partial
                # print("incomplete read %s" % partial)
                have_read = have_read + partial
                self._current_segment = None
                if seg.eof:
                    self.eof = True
                break
            except Exception as exc:
                self.closed_future.set_exception(exc)
                have_read = have_read + partial
                break
            else:
                n_read = len(seg_read)
                # print("Read %d from segment" % n_read)
                if n_read is seg.len:
                    # print("Reached EOF")
                    self._current_segment = None
                    seg_eof = seg.eof
                    if seg_eof:
                        self.eof = seg_eof
                to_read = inf if to_read == inf else to_read - n_read
                if to_read is int(0):
                    break
        return have_read

    async def readline(self) -> Tdata:
        return await self.readuntil(self.line_separator)

    async def readexactly(self, n: int) -> Tdata:
        return super().readexactly(n)

    async def readuntil(self, separator: Optional[Tdata] = None) -> Tdata:
        return super().readuntil(separator)

    async def aclose(self):
        return super().aclose()

    def close_sync(self):
        return super().aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, tb):
        await self.aclose()
