#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GRB Reconstructor process

http://www.goes-r.gov/users/docs/PUG-GRB-vol4-verC.pdf

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

from grbr.cache import product_tmpname
from grbr.parsing import parse_bundle, parse_bundle_file
from grbr.config import CSPP_GEO_GRBR_TIMEOUT
from grbr.messaging import receive_file_offset
from grbr.apid import apid2instr
from grbr.config import CSPP_GEO_GRBR_TOSS_FAILED_VALIDATION
from grbr.config import CSPP_GEO_GRBR_TOSS_FAILED_CRC

from grbr.apid import ABI, GLM, MAG, SEISS, EXIS, SUVI, INFO
import grbr.abi
import grbr.glm
import grbr.mag
import grbr.seiss
import grbr.exis
import grbr.suvi
import grbr.info

import os
import signal
import traceback
import sys

import logging
LOG = logging.getLogger('GRB-R')

CCSDS_CACHE = {}
DATASETS = {}


def reconstruct_bundle_file(filename):
    LOG.info("Reconstructing file %s" % filename)
    counter = 0
    fobj = open(filename, 'rb')
#    mmmap = mmap.mmap(fobj.fileno(), 0, access=mmap.ACCESS_READ)
    for h1, h2, hp, p, length in parse_bundle_file(fobj,
                                                   safe_validation=CSPP_GEO_GRBR_TOSS_FAILED_VALIDATION, 
                                                   safe_crc=CSPP_GEO_GRBR_TOSS_FAILED_CRC, 
                                                   quiet=True):
        signal.alarm(CSPP_GEO_GRBR_TIMEOUT)  # reset our timeout alarm
        LOG.info("Reconstructing sequence #%d" % (counter))
        # catch reconstruction errors and attempt to continue for now
        try:
          reconstruct(h1, h2, hp, p)
        except Exception as e:
          LOG.error("Reconstructing sequence #%d failed:\n%s" % (counter, e))
          traceback.print_exc()
        counter += 1


def reconstruct(h1, h2, hp, p):
    basename = product_tmpname(h1, h2, hp)
    if basename not in DATASETS:
        i = apid2instr(h1.apid)
        if i == ABI:
            DATASETS[basename] = grbr.abi.ABI(h1, h2, hp)
        elif i == GLM:
            DATASETS[basename] = grbr.glm.GLM(h1, h2, hp)
        elif i == SEISS:
            DATASETS[basename] = grbr.seiss.SEISS(h1, h2, hp)
        elif i == MAG:
            DATASETS[basename] = grbr.mag.MAG(h1, h2, hp)
        elif i == EXIS:
            DATASETS[basename] = grbr.exis.EXIS(h1, h2, hp)
        elif i == SUVI:
            DATASETS[basename] = grbr.suvi.SUVI(h1, h2, hp)
        elif i == INFO:
            DATASETS[basename] = grbr.info.INFO(h1, h2, hp)
        else:
            LOG.warning("APID %s not recognized." % (hex(h1.apid)))
            return  # instrument not yet supported...
    DATASETS[basename].add_bundle(h1, h2, hp, p)


def _setup_argparse():
    import argparse
    prog = os.getenv('PROG_NAME', sys.argv[0])
    parser = argparse.ArgumentParser(prog=prog, description="CSPP Geo GRB's GRB-R reconstructor")

    # Required arguments:
    parser.add_argument('input', help='a complete packet bundle file')

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

    logh = logging.StreamHandler()
    logf = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    logh.setFormatter(logf)
    LOG.addHandler(logh)
    LOG.setLevel(levels[verbosity])
    
    # by defining the alarm handler here, we can remove the fifo when we
    # exit and allow ourselves to pick it up again later
    def _alarm_handler(signum, frame):
        for k in DATASETS.keys():
            DATASETS[k].handle_timeout()
        LOG.error("Timeout occurred after %d seconds." % (CSPP_GEO_GRBR_TIMEOUT))
        exit(1)  # bail out and leave everything on the floor

    if os.path.exists(args.input):
        # required to set the alarm handler
        signal.signal(signal.SIGALRM, _alarm_handler)
        signal.alarm(CSPP_GEO_GRBR_TIMEOUT)  # initialize our timeout alarm
        reconstruct_bundle_file(args.input)

    else:
        LOG.error("%s does not exist!" % args.input)
        exit(1)
