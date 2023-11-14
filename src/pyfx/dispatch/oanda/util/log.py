"""Logging utilities"""

import configparser as cf
import logging.config
import logging
import os
from immutables import Map
import sys

from typing import Any, Mapping, Optional
from typing_extensions import TypeAlias

from .paths import Pathname, expand_path

LogConfig: TypeAlias = Mapping[str, Any]
LogConfigDefaults: TypeAlias = Mapping[str, LogConfig]

LOGGER_DEFAULTS: Map[str, LogConfig] = Map(
    logger_hpack = dict(level = logging.WARNING),
    logger_root = dict(level = logging.INFO)
    )

LOGGER_DEFAULT_PROFILE: Pathname = "console_debug_logger.ini"

def configure_loggers(
    config: Optional[Pathname] = None,
    formatter_defaults: Optional[LogConfigDefaults] = None,
    handler_defults: Optional[LogConfigDefaults] = None,
    logger_defaults: Optional[LogConfigDefaults] = LOGGER_DEFAULTS,
    filter_defaults: Optional[LogConfigDefaults] = None
    ):
    global LOGGER_DEFAULT_PROFILE

    config_ini = expand_path(config or LOGGER_DEFAULT_PROFILE, os.path.dirname(__file__))
    if not os.path.exists(config_ini):
        sys.stderr.print("configure_loggers: File not found: %s", config_ini)
        return False

    defaults = dict()
    if formatter_defaults:
        defaults['formatters'] = formatter_defaults
    if handler_defults:
        defaults['handlers'] = handler_defults
    if logger_defaults:
        defaults['loggers'] = logger_defaults
    if filter_defaults:
        defaults['filters'] = filter_defaults

    logging.config.fileConfig(config_ini, disable_existing_loggers=False, defaults=defaults)


__all__  = "LogConfig", "LogConfigDefaults", "LOGGER_DEFAULTS", "configure_loggers"
