#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Debug helper for sorting GRB space packets.

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

import os
import mmap
import logging
import argparse

from parsing import parse_packet

LOG = logging.getLogger(__name__)


def sortem(infile):
    LOG.info("Loading %s" % infile)
    fobj = open(infile, 'rb')
    mmmap = mmap.mmap(fobj.fileno(), 0, access=mmap.ACCESS_READ)
    start = end = 0

    while start < mmmap.size():  # yolo
        LOG.debug("~~~~~~~~~~_^ A WILD PACKET APPEARED!!! ^_~~~~~~~~~~")
        start = end
        h1, h2, hp, _ = parse_packet(mmmap, start)

        end = start + h1.data_length + 7

        LOG.debug("start: %s, end: %s" % (start, end))

        if start == end:
            LOG.error("cursor not incrementing, exit")
            exit(1)

        filename = hex(h1.apid) + ".ccsds"

        f = open(filename, 'ab')
        packet = mmmap[start: end]
        f.write(packet)
        f.close()


def _setup_argparse():
    parser = argparse.ArgumentParser(description="GRB packet bundle sorter")

    # Required arguments:
    parser.add_argument('files', nargs=argparse.REMAINDER,
                        help='CCSDS packet bundle files')

    # Optional arguments:
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

    # Process input
    for input in args.files:
        if os.path.exists(input):
            #      LOG.info("~~~ SORTING %s ~~~" % (input))
            sortem(input)
        else:
            LOG.error("File does not exist: %s" % input)
