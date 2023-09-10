
import logging.config
import os
import sys

def configure_debug_logger():
    debug_ini = os.path.join(os.path.dirname(os.path.abspath(__file__)), "debug_logger.ini")
    if not os.path.exists(debug_ini):
        sys.stderr.print("File not found: %s", debug_ini)
        return False
    return logging.config.fileConfig(debug_ini, disable_existing_loggers=False)
