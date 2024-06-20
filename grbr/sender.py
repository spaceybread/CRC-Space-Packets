#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GRB Sender process (for testing)

Copyright © 2014-2018 University of Wisconsin Regents

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

from parsing import parse_bundle_file

import mmap
import time

import logging
LOG = logging.getLogger('GRB-R')


def send(i, o, sleep=0):
    iobj = open(i, 'rb')
    full_buffer = iobj.read()
    iobj.close()

    oobj = open(o, 'wb', buffering=0)
    iobj = open(i, 'rb', buffering=0)

    buffer_offset = 0
    for h1, h2, hp, p, seq_length in parse_bundle_file(iobj, quiet=True):
        oobj.write(full_buffer[buffer_offset : buffer_offset + seq_length])
        time.sleep(float(sleep))
        buffer_offset = buffer_offset + seq_length

    iobj.close()
    oobj.close()


def _setup_argparse():
    import argparse
    parser = argparse.ArgumentParser(
        description="GRB-R sender process.")

    # Required arguments:
    parser.add_argument('input', help="a ccsds bundle file to read in")
    parser.add_argument('output', help="where you'd like that file written out to")

    # Optional arguments:
    parser.add_argument('-s', '--sleep', dest='sleep', action="store", default=0,
                        help="number of seconds to sleep between writing each packet")
    parser.add_argument('-v', '--verbose', dest='verbosity', action="count", default=0,
                        help='each occurrence increases verbosity through ERROR, WARNING, INFO, DEBUG')

    return parser

if __name__ == '__main__':
    # Get input args
    parser = _setup_argparse()
    args = parser.parse_args()

    # Setup logging
    levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    verbosity = min(args.verbosity, len(levels) - 1)
    logging.basicConfig(level=levels[verbosity])

    send(args.input, args.output, sleep=args.sleep)
