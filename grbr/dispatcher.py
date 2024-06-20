#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Dispatcher to farm out GRB recovery processes

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
import subprocess
import signal

import cache
from parsing import parse_bundle_file
from config import CSPP_GEO_GRB_HOME, CSPP_GEO_GRBR_TMP, CSPP_GEO_GRBR_TIMEOUT
from messaging import send_file_offset
import reconstructor

import logging
LOG = logging.getLogger('GRB-R')

RECONSTRUCTOR = os.path.join(CSPP_GEO_GRB_HOME, "/GRB-R/src/grbr/reconstructor.py")

def _dump_struct(astruct):
    for field_name, field_type, bitcount in astruct._fields_:
        LOG.debug("%s: %s" % (field_name, getattr(astruct, field_name)))


def _alarm_handler(signum, frame):
    LOG.error("Timeout occurred after %d seconds." % (CSPP_GEO_GRBR_TIMEOUT))
    exit(-1)

# required to set the alarm handler
signal.signal(signal.SIGALRM, _alarm_handler)


def dispatch_grb(infile, nopipe=False):
    LOG.info("Dispatching from %s" % infile)
    fobj = open(infile, 'rb')
    mmmap = mmap.mmap(fobj.fileno(), 0, access=mmap.ACCESS_READ)
    start = 0
    for h1, h2, hp, p, length in parse_bundle_file(mmmap, quiet=True):
        signal.alarm(CSPP_GEO_GRBR_TIMEOUT)  # reset our timeout alarm
        if hp is not None:
            if nopipe:
                reconstructor.reconstruct(h1, h2, hp, p)
            else:
                basepath = os.path.join(
                    CSPP_GEO_GRBR_TMP, cache.product_tmpname(h1, h2, hp))
                fifopath = basepath + ".pipe"
                try:
                    # this throws OSError if it exists already, and skips the
                    # rest
                    os.mkfifo(fifopath)
                    log = open(basepath + ".log", 'w', 1)  # line buffered
                    subprocess.Popen(
                        ["python", RECONSTRUCTOR, '-vv', fifopath], stdout=log, stderr=subprocess.STDOUT)
#          subprocess.Popen(["python", "-m", "trace", "-t", RECONSTRUCTOR, '-vvvv', fifopath], stdout=log, stderr=log)
                    LOG.info("Spawned and started reconstructor on: %s", fifopath)
                except OSError, e:
                    LOG.info(
                        "FIFO already exists, so we'll just write to it: %s", fifopath)

                send_file_offset(fifopath, infile, start)
        start = start + length

def _setup_argparse():
    import argparse
    parser = argparse.ArgumentParser(description="GRB-R dispatcher - a dispatcher for farming out reconstructor processes.")

    # Required arguments:
    parser.add_argument('files', nargs=argparse.REMAINDER, help='any number of CCSDS packet bundle files')

    # Optional arguments:
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False, help='debug mode, call reconstructor directly (no subprocess/messaging)')
    parser.add_argument('-v', '--verbose', dest='verbosity', action="count", default=0, help='each occurrence increases verbosity through ERROR, WARNING, INFO, DEBUG')

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
            dispatch_grb(input, args.debug)
        else:
            LOG.error("File does not exist: %s" % input)
