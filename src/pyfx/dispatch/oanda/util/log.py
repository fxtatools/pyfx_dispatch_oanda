"""Logging utilities"""

import io
import logging.config
import logging
import logging.handlers
import multiprocessing as mp
import queue

from typing import Iterable, Optional, Union


def log_formatter() -> logging.Formatter:
    """Create a log formatter

    The log formatter will provide formatting for the following fields:
    Process ID; Timestamp for the LogRecord, including milliseconds;
    Thread ID; Logger name and log level; Message text and optional
    exception information.

    Returns:
        logging.Formatter: A new log formatter
    """
    return logging.Formatter(
        "[%(process)d %(asctime)s.%(msecs)d %(thread)x] [%(name)s] [%(levelname)s] %(message)s",
        datefmt="%F %X"
    )


def queue_handler(queue: Union[mp.Queue, queue.Queue, queue.SimpleQueue],
                  formatter: Optional[logging.Formatter] = None,
                  ) -> logging.handlers.QueueHandler:
    """Create a logging queue handler

    Args:
        queue (Union[mp.Queue, queue.Queue, queue.SimpleQueue]):
            LogRecord Queue for the handler

        formatter (Optional[logging.Formatter], optional):
            Optional formatter. If not provided, a formatter will
            be created with `log_formatter()`

    Returns:
        logging.handlers.QueueHandler: A new logging handler
    """
    recordq = queue or mp.Queue()
    handler = logging.handlers.QueueHandler(recordq)
    handler.formatter = formatter or log_formatter()
    return handler

def console_handler(stream: Optional[io.IOBase],
                    formatter: Optional[logging.Formatter] = None,
                    ) -> logging.StreamHandler:
    handler = logging.StreamHandler(stream) if stream else logging.StreamHandler(stream)
    handler.formatter = formatter or log_formatter()
    return handler


def configure_logger(name: Optional[str] = None,
                     level: Optional[Union[int, str]] = None,
                     handlers: Optional[Union[logging.Handler, Iterable[logging.Handler]]] = None,
                     handlers_override: bool = False
                     ) -> logging.Logger:
    """Configure a logger

    Args:
        name (Optional[str], optional):
            Logger name. If not provided, the root logger will be configured

        level (Optional[Union[int, str]], optional):
            Optional log level, if provided

        handlers (Optional[list[logging.Handler]], optional):
            Optional handlers for the logger

        handlers_override (bool, optional):
            When a `handlers` list is provided, indicates whether to override
            the existing handlers for the logger. If true, any previous list
            of handlers  will be removed from the logger - in effect, replaced
            with the provided `handlers` list. Otherwise, the logger's handlers
            list will be  extended with the provided `handlers`.

    Returns:
        logging.Logger: The logger, as selected per the value of `name`
    """
    logger = logging.getLogger(name) if name else logging.getLogger()
    if level:
        logger.setLevel(level)
    if handlers:
        if handlers_override:
            logger.handlers = [handlers] if isinstance(handlers, logging.Handler) else list(handlers)
        elif isinstance(handlers, Iterable):
            for hdl in handlers:
                logger.addHandler(hdl)
        else:
            logger.addHandler(handlers)
    return logger


__all__ = (
    "log_formatter", "queue_handler", "console_handler", "configure_logger"
)
