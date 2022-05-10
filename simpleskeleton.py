#!/usr/bin/env python

import argparse
import fcntl
import os
import subprocess
import sys
from typing import NamedTuple, Optional, TypeVar

HELP = """
simpleskeleton.py by Preston Hunt <me@prestonhunt.com>
https://github.com/presto8/pythonskeletonsimple

A simple single-file Python boilerplate for writing simple command-line shell
scripts.
"""


def parse_args():
    parser = argparse.ArgumentParser(description=HELP, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('paths', nargs='*', help='paths to process')
    parser.add_argument('--verbose', default=False, action='store_true', help='show more detailed messages')
    return parser.parse_args()


def main():
    mutex()
    if ARGS.verbose:
        print("verbose mode enabled, will display abspath")
    for path in ARGS.paths:
        print(worker(path))


def mutex():
    this_script = os.path.realpath(__file__)
    lockfd = os.open(this_script, os.O_RDONLY)
    try:
        fcntl.flock(lockfd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise Fail(f"{this_script} is already running")


def scantree(path, follow_symlinks=False, recursive=True):
    passthru = [follow_symlinks, recursive]
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=follow_symlinks) and recursive:
            yield from scantree(entry.path, *passthru)
        else:
            yield entry


# From: https://github.com/facebook/pyre-check/blob/master/pyre_extensions/__init__.py#L7-L8
_T = TypeVar("_T")


def none_throws(optional: Optional[_T], message: str = "Unexpected `None`") -> _T:
    """Convert an optional to its value. Raises an `AssertionError` if the
    value is `None`"""
    if optional is None:
        raise AssertionError(message)
    return optional


class ParsedPath(NamedTuple):
    ok: bool
    input_path: str
    basename: str
    abspath: str


def parse_path(path) -> ParsedPath:
    result = dict(ok=False, input_path=path)
    result['basename'] = os.path.basename(path)
    result['abspath'] = os.path.abspath(path)
    result['ok'] = True
    return ParsedPath(**result)


def worker(path) -> str:
    ppath = parse_path(path)
    if ARGS.verbose:
        print(ppath)
    return ppath.abspath if ARGS.verbose else ppath.basename


def run(*args):
    return subprocess.run(args, capture_output=True, text=True)


class Fail(Exception):
    pass


if __name__ == '__main__':
    try:
        # Command-line arguments are considered as immutable constants of the
        # universe, and thus are globally available in this script.
        ARGS = parse_args()
        main()
    except Fail as f:
        print(*f.args, file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("Ctrl+C")
