Examples - pyfx.dispatch.oanda
==============================

## Overview

The following example scripts are available

**`quotes.py`** : Illustration of direct I/O within an asynchronous
context manager, printing latest quotes information for all available
market symbols.

**`quotes_async.py`**  : Example using asynchronous callbacks.

**Implementation Notes**

* The `async` example uses the HTTP/2 and asyncio support available with
  [HTTPX][httpx] and [HTTPCore][httpcore].

* For creating an asynchronous stream onto each of the `stdout` and `stderr`
  descriptors, the `ascync` example applies [aioconsole][aioconsole].

* The `async` example may be generally more responsive under console I/O, given
  the asynchronous callbacks used for accessing and printing each series of
  market symbol quotes

* Additional optimizations may be enabled when running the example scripts
  under `python -O` i.e without `__debug__`

* Both examples will use the same v20 endpoint under the configured `host` URL

## Configuration Data Format

The examples in this directory will use an `account.ini` file
for configuration. This file must exist in the same directory
as the example scripts.

The configuration syntax is described in the [main README](../README.md#example-scripts)


## Optimizations and Debugging

Run with debug logging:
```sh
DEBUG=defined python3 quotes.py
DEBUG=defined python3 quotes_async.py
```

Run without debugging:
```sh
python3 -O quotes.py
python3 -O quotes_async.py
```

Run with [faulthandler][faulthandler] activated, under
[Python Development Mode][pydevmode].
```sh
PYTHON="PYTHONMALLOC=debug PYTHONASYNCIODEBUG=1 python3 -W default -X faulthandler"
${PYTHON} quotes.py
${PYTHON} quotes_async.py
```

The [faulthandler][faulthandler] support may be of use when debugging at
the application or platform scope. For instance, a segfault may occur in
relation to the Python IOCP support on Microsoft Windows, subsequent of an
abnormal exit from or termination of the asyncio event loop - as utilized
together with asyncio networking support, in these examples - mainly, after
an uncaught exception within some asyncio task.


[httpx]: https://www.python-httpx.org/
[httpcore]: https://www.encode.io/httpcore/
[aioconsole]: https://github.com/vxgmichel/aioconsole
[faulthandler]: https://docs.python.org/3/library/faulthandler.html#module-faulthandler
[pydevmode]: https://docs.python.org/3/library/devmode.html#devmode
