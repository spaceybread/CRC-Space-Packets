#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple tool for checking the validity of a CCSDS bundle file.

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

import os
import mmap
import argparse

import logging
LOG = logging.getLogger('GRB-R')


def validate_file(infile):
    print("Loading %s" % (infile))
    fobj = open(infile, 'rb')
    mmmap = mmap.mmap(fobj.fileno(), 0, access=mmap.ACCESS_READ)
    counter = 0
    for i in parse_bundle_file(mmmap):
        counter += 1
    print("Validated %d packet bundles from %s" % (counter, infile))

def _setup_argparse():
    parser = argparse.ArgumentParser(
        description="GRB-R validator - a validator to discover problems with CCSDS packet bundles.")

    # Required arguments:
    parser.add_argument('files', nargs=argparse.REMAINDER,
                        help='any number of CCSDS packet bundle files')

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
            validate_file(input)
        else:
            LOG.error("File does not exist: %s" % input)
