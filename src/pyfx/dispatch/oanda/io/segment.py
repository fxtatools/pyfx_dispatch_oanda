"""Segmented I/O streams"""

import asyncio as aio
import concurrent.futures
from enum import IntEnum, Enum
import os
from queue import SimpleQueue, Empty
import sys
from typing import Awaitable, Generic, Iterator, Literal, Optional, Union
from typing_extensions import Generic, TypeVar

Tdata = TypeVar("Tdata", bound=Collection)


class ReaderConst(float, Enum):
    INF = float("inf")


class IoState(IntEnum):
    NONE = 0
    CLOSED = 1


class DataError(Exception):
    pass


class EndOfFile(DataError):
    pass


class ClosedError(DataError):
    pass


class Segment(Generic[Tdata]):
    """chunk-oriented input buffer for segmented `read()`

    Synchronous Segment implementation
    """

    __slots__ = "data", "slen", "cursor", "last", "eof"

    data: Tdata
    """Segment Data

    The segment `data` value will contain zero or more elements
    within a value of the type, `Tdata`. generally immutable
    """

    slen: int
    """Segment Length

    The memoized length of the `data` segment, generally immutable
    """

    cursor: int
    """Cursor for read

    A mutable value, this slot may be updated for the segment, during read()

    ### Known Limitations

    The Segment API does not provide locking support for concurrent modification
    of the `Segment.cursor` property. It's assumed that this value will be modified
    by a `read()` operation in at most one thread
    """

    eof: bool
    """EOF indicator

    EOF flag value, indicating whether the end of this `data` segment
    represents end of file for the containing semgent channel, generally
    immutable
    """

    def __init__(self, data: Tdata, eof: bool = False):
        self.data = data
        self.slen = len(data)
        self.eof = eof
        self.cursor = 0

    def read(self, n: Union[int, Literal[ReaderConst.INF]] = -1) -> Tdata:
        data = self.data
        last = self.slen
        if n < 0 or n is ReaderConst.INF:
            rslt = data[self.cursor:]
            self.cursor = last
            return rslt
        else:
            cursor = self.cursor
            end = cursor + n
            if end > last:
                raise aio.IncompleteReadError(expected=n, partial=data[cursor:last])
            else:
                rslt = data[self.cursor: end]
                self.cursor = end
                return rslt


T_seg_co = TypeVar("T_seg_co", bound=Segment, covariant=True)


class SegmentChannelBase(Generic[T_seg_co, Tdata]):
    # fmt: off
    __slots__ = ("read_queue", "closed_future", "eof",
                 "empty_sequence", "line_separator",
                 "current_segment",
                 )
    # fmt: on

    eof: bool
    """EOF indicator

    a flag value, indicating whether the segment channel has processed
    a Segment with `Segment.eof == True`
    """

    empty_sequence: Tdata
    """Empty sequence for this segment channel

    This value represents the "Empty sequence" for the segment channel,
    such that will be returned on null read.

    If not set in the constructor, the value will be set to an empty
    subset of the first segment value provided to `feed()`
    """

    line_separator: Tdata
    """Line separator

    This value will be used for line-oriented I/O within the segment channel
    """

    read_queue: SimpleQueue
    """Segment queue

    This slot is implemented with a SimpleQueue, a synchronouos Queue class.
    This class provides a generally thread-safe implementation for concurrent
    `feed()` and `read()` calls.

    This implementation entails an assumption that each of the `feed()`
    and `read()` methods will be accessed within at most one concurrent
    thread, respectively.
    """

    def __init__(
        self,
        empty_sequence: Optional[Tdata] = None,
        line_separator: Tdata = os.linesep,  # type: ignore
    ):
        self.eof = False
        self.current_segment = None
        self.line_separator = line_separator

        if not hasattr(self, "read_queue"):
            ## may be overridden in a subclass
            self.read_queue = SimpleQueue[Segment[Tdata]]()

        if empty_sequence:
            ## if not provided here, empty_sequence will be set with the first
            ## call to feed() such as to use the same sequence type
            ## as the first sequence provided to feed()
            self.empty_sequence = empty_sequence

    def close(self):
        """Closes this segment channel

        - Sets the `eof` state of the segment channel to True
        - Sets the result of the `closed_future` to `IoState.Closed`, if the
          `closed_future` was not previously in a "done" state
        """
        self.eof = True
        try:
            self.closed_future.set_result(IoState.Closed)
        except:  # nosec B110
            pass

    def closed(self):
        """Return true if this segment channel is closed

        `closed()` will return true when the `closed_future` for the segment channel
        is in a "done" state
        """
        return self.closed_future.done()

    def next_segment(self) -> Optional[Segment[Tdata]]:
        seg: Segment[Tdata] = self.current_segment
        delay = sys.getswitchinterval()
        while seg is None:
            if self.closed() or self.eof:
                return None
            else:
                try:
                    seg = self.read_queue.get(timeout=delay)
                except Empty:
                    pass
        self.current_segment = seg
        return seg

    def peek_segment(self) -> Tdata:
        """return the next segment data, without advancing cursor"""
        ## usage: provides support for effective read-ahead,
        ## assuming a certain synchronization across channel I/O
        seg = self.next_segment()
        return seg.data if seg else self.empty_sequence

    def finalize_segment(self, seg):
        ## utility method for read()
        if seg.eof:  # and seg.cursor == seg.slen
            self.eof = True
        # self.read_queue.task_done()
        self.current_segment = None
        # del seg

    def queued(self) -> Iterator[Tdata]:
        """Return an iterator yielding all queued segments until `self.eof` or `self.closed()`

        Implementation Notes

        This method should generally not be mixed with applications
        of `channel.read()` onto the same segment channel. For any active segment in the
        channel, the iterator will provide the segment's unabridged data, regardless of
        cursor position. Any data previously accessed from the active segment with `read()`
        will be duplicated in the return value, for any active segment under `queued()`.

        The iterator will exit under the following events:
        1) after yielding a segment that was provided as `channel.feed(<data>, eof=True)`
        2) before any subsequent iteration, once the  segment channel is `closed()`

        This iterator is generally thread-safe, under the following limitations:

        1) `channel.feed()` may be called within zero or more threads for the
           synchronous implementation, or at most one thread for the async
           implementation.

        2) `channel.queued()` may be called in at most one thread, within
           either implementation. In both implementations, this thread may
           be distinct to the thread calling `channel.feed()`

        If no new data has been provided to the channel as with `channel.feed()`,
        the iterator will block within the current thread, until the first
        segment has been provided. Subsequently, after yielding the data
        of the current segment, if the channel is not closed and no `eof` segment
        has been provided to `feed()`, the iterator will block until the next segment.
        """
        queue = self.read_queue
        try:
            while not self.closed():
                seg = self.current_segment
                if seg is None:
                    if self.eof or self.closed():
                        return
                    seg = queue.get()
                yield seg.data
                self.finalize_segment(seg)
        finally:
            if not self.closed():
                self.close()

    def join_queued(self, sep: Tdata) -> Tdata:
        return sep.join(self.queued())


class SegmentChannel(SegmentChannelBase[Segment[Tdata], Tdata]):
    """synchronous segment channel implementation

    As a segment-oriented analogy to `write()`, the SegmentChannel `feed()`
    method will deliver sucessive sequence values of the type `Tdata`
    to be processed under `read()`.

    The stream-lke `read()` method will  process the effective concatenation
    of input values delivered via `feed()`

    ### Async Support

    A segment channel implementation for asyncio is avaialble in the
    AsyncSegmentChannel class.

    ### Known Limitations

    The `feed()` and `read()` methods are considered generally thread-safe,
    for concurrent access in at most one thread for each respective method.

    This assumption of thread safety is predicated mainly on the implementation
    of the `read_queue` slot for the class. The read queue  should provide a
    thread-safe queue for segment delivery via at most one thread calling `feed()`,
    with concurrent access in at most one thread calling `read()`

    All input values provided to `feed()` should be of the same type, e.g
    `bytes` or `str`. This type is denoted in the `Tdata` generic parameter.
    """

    current_segment: Optional[Segment[Tdata]]  # type: ignore
    """Current Segment

    This slot provides a segment pointer for `read()`. When None, the next
    `read()` operation will poll the `read_queue` for a next segment.
    """

    closed_future: concurrent.futures.Future
    """Closed state

    a concurrent Future, indicating whether the reader is closed
    """

    def __init__(
        self,
        empty_sequence: Optional[Tdata] = None,
        line_separator: Tdata = os.linesep,  # type: ignore
        closed_future: Optional[concurrent.futures.Future] = None,
    ):
        super().__init__(empty_sequence, line_separator)

        if closed_future:
            self.closed_future = closed_future
        elif not hasattr(self, "closed_future"):
            ## default may be overridden in a subclass
            self.closed_future = concurrent.futures.Future()

        if empty_sequence:
            ## if not provided here, empty_sequence will be set with the first
            ## call to feed() such as to use the same sequence type
            ## as the first sequence provided to feed()
            self.empty_sequence = empty_sequence

    def __repr__(self):
        return "<%s [%s] at 0x%x>" % (
            self.__class__.__name__,
            self.closed_future,
            id(self),
        )

    def at_eof(self) -> bool:
        ## this method was defined originally for the asyncio StreamReader protocol
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
        return self.feed(data + self.line_separator, eof)  # type: ignore

    def read(self, n: int = -1) -> Tdata:
        ## synchronous read()
        ##
        ## this implementation is generally shadowed with asynchronous read()
        ## in the AsyncSegmentChannel implementation
        to_read = n if n >= 0 else ReaderConst.INF
        have_read = self.empty_sequence if hasattr(self, "empty_sequence") else None
        while to_read >= 0:
            seg = self.next_segment()
            if not have_read:
                # map have_read to empty_sequence after the first stream feed()
                have_read = self.empty_sequence
            if not seg:
                return have_read
            try:
                seg_read = seg.read(to_read)  # type: ignore
                have_read = have_read + seg_read  # type: ignore
            except aio.IncompleteReadError as exc:
                partial = exc.partial
                have_read = have_read + partial  # type: ignore
                self.finalize_segment(seg)
                break
            except Exception as exc:
                self.closed_future.set_exception(exc)
                break
            else:
                n_read = len(seg_read)
                if n_read == seg.slen:
                    self.finalize_segment(seg)
                if to_read is not ReaderConst.INF:
                    to_read = to_read - n_read
                if to_read == 0:
                    break
        return have_read  # type: ignore

    def readline(self) -> Tdata:
        return self.readuntil(self.line_separator)

    def readexactly(self, n: int) -> Tdata:
        assert n >= 0, "n is a negative value"  # nosec B101
        rslt = self.read(n)
        if len(rslt) is not int(n):
            raise aio.IncompleteReadError(partial=rslt, expected=n)  # type: ignore
        else:
            return rslt

    def readuntil(self, separator: Optional[Tdata] = None) -> Tdata:
        raise NotImplementedError(self.readuntil)

    def __enter__(self):
        """Synchronous context manager entry method

        This context manager entry method will return the bound
        segment channel
        """
        return self

    def __exit__(self, exc_type, exc_value, tb):
        """Synchronous context manager exit method

        This context manager exit method will close the bound segment channel
        """
        self.close()


## The original async implementation - AsyncSegmentChannel


class AsyncSegment(Segment[Tdata]):
    """async wrapper for the Segment class

    This class provides an async wrapper for `Segment.read()`, for
    application in `AsyncSegmentChannel.read()`
    """

    async def read(self, n: int = -1) -> Awaitable[Tdata]:  # type: ignore
        return super().read(n)  # type: ignore


class AsyncSegmentChannel(SegmentChannelBase[AsyncSegment[Tdata], Tdata]):
    """asynchronous segment channel

    This class provides an asynchronous implementation for SegmentChannel I/O methods
    - `feed()`
    - `feed_line()`
    - `read()`
    - `readline()`
    - `readuntil()`

    The `aclose()` method is provided as a matter of convention. This method dispatches
    to synchronous `close()`.
    """

    current_segment: Optional[AsyncSegment[Tdata]]  # type: ignore
    """Current segment for this async channnel"""

    read_queue: SimpleQueue[AsyncSegment[Tdata]]  # type: ignore
    """Segment read queue for this async channel"""

    closed_future: aio.Future  # type: ignore
    """Closed state for this async channel

    Implemented for AsyncSegmentChannel using an aio.Future, this value
    provides an effective indicator for channel "closed" state.
    """

    def __init__(
        self,
        empty_sequence: Optional[Tdata] = None,
        line_separator: Tdata = os.linesep,  # type: ignore
        closed_future: Optional[aio.Future] = None,
        loop: Optional[aio.AbstractEventLoop] = None,
    ):
        # global thread_loop
        if closed_future:
            self.closed_future = closed_future
        else:
            self.closed_future = aio.Future(
                loop=loop if loop else aio.get_running_loop() or aio.get_event_loop_policy().get_event_loop()
            )

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
            ## This call would generally not block unless the queue
            ## has been replaced with a bounded queue in some subclass
            self.read_queue.put(AsyncSegment(data, eof))

    async def anext_segment(self) -> Optional[Segment[Tdata]]:
        seg: Segment[Tdata] = self.current_segment
        delay = sys.getswitchinterval()
        while seg is None:
            if self.closed():
                return None
            else:
                try:
                    async with aio.timeout(delay):
                        seg = self.read_queue.get()
                except aio.TimeoutError:
                    pass
                except aio.CancelledError:
                    return None
        self.current_segment = seg
        return seg

    async def feed_line(self, data: Tdata, eof: bool = False):
        return await self.feed(data + self.line_separator, eof)  # type: ignore

    async def read(self, n: int = -1) -> Awaitable[Tdata]:  # type: ignore
        to_read = n if n >= 0 else ReaderConst.INF
        have_read = self.empty_sequence if hasattr(self, "empty_sequence") else None
        queue = self.read_queue
        while to_read >= 0:
            seg = self.current_segment
            if seg is None:
                if self.eof or self.closed():
                    return have_read  # type: ignore
                seg = await self.anext_segment()
                self.current_segment = seg
            if not have_read:
                # map have_read to empty_sequence after the first stream feed()
                have_read = self.empty_sequence
            try:
                seg_read = await seg.read(to_read)  # type: ignore
                have_read = have_read + seg_read  # type: ignore
            except aio.IncompleteReadError as exc:
                partial = exc.partial
                have_read = have_read + partial  # type: ignore
                self.finalize_segment(seg)
                break
            except Exception as exc:
                self.closed_future.set_exception(exc)
                break
            else:
                n_read = len(seg_read)  # type: ignore
                if n_read == seg.slen:
                    self.finalize_segment(seg)
                to_read = to_read if to_read == ReaderConst.INF else to_read - n_read
                if to_read == 0:
                    break
        return have_read  # type: ignore

    async def readline(self) -> Awaitable[Tdata]:  # type: ignore
        return await self.readuntil(self.line_separator)

    async def readexactly(self, n: int) -> Awaitable[Tdata]:  # type: ignore
        assert n >= 0, "n is a negative value"  # nosec B101
        rslt = await self.read(n)
        if len(rslt) is not int(n):  # type: ignore
            raise aio.IncompleteReadError(partial=rslt, expected=n)  # type: ignore
        else:
            return rslt

    async def readuntil(self, separator: Optional[Tdata] = None) -> Awaitable[Tdata]:  # type: ignore
        raise NotImplementedError(self.readuntil)

    def close(self) -> aio.Handle:
        """Closes this segment channel

        - Sets the `eof` state of this channel to True

        - Sets the result of the `closed_future` to `IoState.Closed` if the
          `closed_future` was not previously in a "done" state.

        `close()` will endeavor to set the IoState for the `closed_future`
        using a thread-safe call.

        Returns an asyncio.Handle for the thread-safe call to set the result
        of the `closed_future`. This handle may result in an exception when
        awaited, of a type `aio.InvalidStateException`, if the `closed_future`
        was previously in a "done" state.
        """
        self.eof = True
        # task = self.closed_future.get_loop().create_task(self.aclose())
        # _ = task.result
        self.close_current()

    def close_current(self):
        ""
        try:
            if not self.closed_future.done():
                self.closed_future.set_result(IoState.CLOSED)
        except aio.InvalidStateError:
            pass

    async def aclose(self):
        """Set the eof state for the channel to `True` and ensure a "done" state
        for the channel's `closed_future`.

        If the `closed_future` was initialized under a different loop than the loop
        calling this coroutine, then the "done" state will be set for the `closed_future`
        under a thread-safe call, using the future's original event loop. In otherwise,
        the "done" state will be set as for a future initialized within the same event
        loop as current.

        If not already set, the state will be set to the value `IoState.CLOSED`
        """
        self.eof = True
        ftr = self.closed_future
        ftr_loop = ftr.get_loop()
        running_loop = None
        try:
            running_loop = aio.get_running_loop()
        except RuntimeError:
            pass
        try:
            if ftr_loop is running_loop:
                self.close_current()
            elif ftr_loop.is_running():
                hdl = ftr_loop.call_soon_threadsafe(self.close_current)
                # await ftr
        except aio.InvalidStateError:
            pass

    async def __aenter__(self):
        """Asynchronous context maanger entry method

        returns this segment channel
        """
        return self

    async def __aexit__(self, exc_type, exc_value, tb):
        """Asynchronous context maanger exit method

        closes this segment channel, as with `aclose()`
        """
        try:
            await self.aclose()
        except:
            self.close_current()
            raise
