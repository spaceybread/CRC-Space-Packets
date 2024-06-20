#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utility to convert a CCSDS bundle to a simple netCDF file
for CSPP Geo GRB package testing.

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

import mmap
import numpy as np
from netCDF4 import Dataset

from sp_structs import parse_packet

import logging
LOG = logging.getLogger(__name__)


def _break_ccsds(ccsds_filename):
    ccsds = open(ccsds_filename, 'rb')
    mmmap = mmap.mmap(ccsds.fileno(), 0, access=mmap.ACCESS_READ)
    start = 0
    p = []
    while start < mmmap.size():  # FIXME: is this the best way to end?
        h1, h2, hp, _ = parse_packet(mmmap, start)
        end = start + h1.data_length + 7
        p.append(mmmap[start:end])
        start = end
    return p


def ccsds2nc(ncfile, ccsds_list):
    nc = Dataset(ncfile, 'w')
    packets = []
    for ccsds_filename in ccsds_list:
        packets += _break_ccsds(ccsds_filename)

    sizes = []
    offsets = []
    o = 0
    for p in packets:
        sizes.append(len(p))
        offsets.append(o)
        o += len(p)

    nc.createDimension('number_of_packets', None)
    nc.createDimension('number_of_data_bytes', None)

    sop = nc.createVariable('size_of_packet', 'i4',
                            dimensions='number_of_packets')[:] = sizes
    otp = nc.createVariable('offset_to_packet', 'i4',
                            dimensions='number_of_packets')[:] = offsets
    gspd = nc.createVariable('grb_space_packet_data', 'i1', dimensions='number_of_data_bytes')[
        :] = np.fromstring(''.join(packets), dtype=np.byte)
    nc.close()


def _setup_argparse():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)

    # Required arguments:
    parser.add_argument('netcdf', help='an output netCDF4 file')
    parser.add_argument('ccsds', nargs=argparse.REMAINDER,
                        help='any number of CCSDS packet bundle files')

    # Optional arguments:
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

    ccsds2nc(args.netcdf, args.ccsds)
