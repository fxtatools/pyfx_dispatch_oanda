## reflection.py

import inspect

from types import FrameType
from typing import Optional, Union


def caller_module(frame: Optional[Union[FrameType, inspect.FrameInfo]] = None):
    cur = frame.frame if isinstance(frame, inspect.FrameInfo) else frame if isinstance(frame, FrameType) else inspect.currentframe()
    if not cur:
        raise RuntimeError("Unable to determine current frame")
    for info in inspect.getouterframes(cur):
        if "__package__" in info.frame.f_locals:
            return info.frame.f_globals["__name__"]


__all__ = ("caller_module",)
