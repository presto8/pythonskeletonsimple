#!/usr/bin/env python

import fcntl
import os
from typing import Optional, TypeVar


class Fail(Exception):
    pass


def mutex():
    this_script = os.path.realpath(__file__)
    lockfd = os.open(this_script, os.O_RDONLY)
    try:
        fcntl.flock(lockfd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise Fail(f"{this_script} is already running")


# From: https://github.com/facebook/pyre-check/blob/master/pyre_extensions/__init__.py#L7-L8
_T = TypeVar("_T")


def none_throws(optional: Optional[_T], message: str = "Unexpected `None`") -> _T:
    """Convert an optional to its value. Raises an `AssertionError` if the
    value is `None`"""
    if optional is None:
        raise AssertionError(message)
    return optional
