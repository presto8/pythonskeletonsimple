#!/usr/bin/env python
"""
simpleskeleton.py by Preston Hunt <me@prestonhunt.com>
https://github.com/presto8/pythonskeletonsimple

A simple single-file Python boilerplate for writing simple command-line shell
scripts.
"""

import argparse
import fcntl
import os
import shelve
import subprocess
import sys
from typing import NamedTuple


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('paths', nargs='*', help='paths to process')
    parser.add_argument('--verbose', default=False, action='store_true', help='show more detailed messages')
    parser.add_argument('--database', default="data.db", help='location of persistent data storage')
    return parser.parse_args()


def main():
    mutex()

    if ARGS.verbose:
        print("verbose mode enabled, will display abspath")

    with shelve.open(ARGS.database, writeback=True) as db:
        if not 'paths' in db:
            db['paths'] = []

        print("previous paths:", db['paths'])

        for path in ARGS.paths:
            db['paths'].append(path)
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
