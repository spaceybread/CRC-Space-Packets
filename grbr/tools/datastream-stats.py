#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple utility to provide datastream stats.

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
from sp_structs import parse_packet

import logging
LOG = logging.getLogger(__name__)


stats = {}
def produce_stats(files):
	for nfile, ncfile in enumerate(sorted(files)):
	    sys.stdout.write("Reading %04d of %04d: %s" % (nfile, len(files), ncfile))
    	nc = Dataset(ncfile, 'r')
    	packets = nc.variables['grb_space_packet_data'][:]
    	offsets = nc.variables['offset_to_packet'][:]
    	sizes = nc.variables['size_of_packet'][:]
	    for i in range(len(sizes)):
	        size = sizes[i]
	        offset = offsets[i]
	        packet = packets[offset:offset + size]
	        packet = packet.astype(np.int8).tostring()
	        h1, h2, hp, p = parse_packet(packet)
	        if h1.apid not in stats:
	        	stats[h1.apid] = 0
	        else:
	        	stats[h1.apid] = stats[h1.apid] + len(p)
	    sys.stdout.write("\r")
	# we should convert APID to INSTR
	print(stats)


def _setup_argparse():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)

    # Required arguments:
    parser.add_argument('ncfiles', nargs=argparse.REMAINDER,
                        help='any number of netCDF4 GRB stream files')

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

    produce_stats(args.ncfiles)
