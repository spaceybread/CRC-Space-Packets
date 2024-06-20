#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utility to separate out CCSDS bundles by their final datasets.

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

import apid
from cache import product_tmpname
from parsing import parse_bundle_file

import os, mmap
import argparse
import logging
LOG = logging.getLogger(__name__)

def _loop_apids(indir, sortfunc):
    for a in apid.apids.keys():
        if sortfunc(a):
            f = os.path.join(indir, hex(a) + ".ccsds")
            if os.path.exists(f):
                try:
                    sortem(f)
                except:
                    LOG.error("sorting %s was unsuccessful" % (f))
                    continue

def loop_dir(indir):
    _loop_apids(indir, apid.isData)
    _loop_apids(indir, apid.isMetadata)


def sortem(infile):
    LOG.info("Loading %s" % infile)
    fobj = open(infile, 'rb')
    mmmap = mmap.mmap(fobj.fileno(), 0, access=mmap.ACCESS_READ)
    start = 0
    for h1, h2, hp, p, length in parse_bundle_file(mmmap):
        filename = product_tmpname(h1, h2, hp) + ".ccsds"

        f = open(filename, 'ab')
#        print "writing %s, [%d : %d] (total %d > h1 %d) of %d to %s" % (hex(h1.apid), start, start+length, length, h1.data_length, len(mmmap), filename)
        packet = mmmap[start:start+length]
        f.write(packet)
        f.close()

        start += length


def _setup_argparse():
    parser = argparse.ArgumentParser(description="GRB packet bundle sorter")

    # Required arguments:
    parser.add_argument('files', nargs=argparse.REMAINDER,
                        help='CCSDS packet bundle files')

    # Optional arguments:
    parser.add_argument('-v', '--verbose', dest='verbosity', action="count", default=0,
                        help='each occurrence increases verbosity through ERROR, WARNING, INFO, DEBUG')
    parser.add_argument('-d', '--directory', dest='directory', action='store_true', default=False,
                        help='input files are treated as directories of CCSDS bundles with standard hex naming scheme like "0x123.ccsds"')
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
            if args.directory:
                loop_dir(input)
            else:
                sortem(input)
        else:
            LOG.error("File does not exist: %s" % input)
