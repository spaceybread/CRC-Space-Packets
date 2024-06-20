#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utility to carve off a chunk of a ccsds bundle.

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

import argparse
import mmap

from sp_structs import parse_packet

import logging
LOG = logging.getLogger(__name__)


def _break_one(ccsds_filename, desired):
    ccsds = open(ccsds_filename, 'rb')
    mmmap = mmap.mmap(ccsds.fileno(), 0, access=mmap.ACCESS_READ)
    start = 0
    count = 0
    p = []
    while count <= desired and start < mmmap.size():  # FIXME: is this the best way to end?
        h1, h2, hp, _ = parse_packet(mmmap, start)
        end = start + h1.data_length + 7
        p.append(mmmap[start:end])
        start = end
        count += 1
    return p


def _break_ccsds(output, ccsds_list, desired):
    out = open(output, 'wb')
    packets = []
    for ccsds_filename in ccsds_list:
        packets += _break_one(ccsds_filename, desired)

    out.write(''.join(packets))
    out.close()


def _setup_argparse():
    parser = argparse.ArgumentParser(description=__doc__)

    # Required arguments:
    parser.add_argument('output', help='the output CCSDS packet bundle')
    parser.add_argument('input', nargs=argparse.REMAINDER,
                        help='any number of CCSDS packet bundle files')

    # Optional arguments:
    parser.add_argument('-n', '--num', dest='num', action='store', default=1,
                        help='number of packets to break off the front of each provided packet bundle')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False,
                        help='debug mode, call reconstructor directly (no subprocess/messaging)')
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

    _break_ccsds(args.output, args.input, args.num)
