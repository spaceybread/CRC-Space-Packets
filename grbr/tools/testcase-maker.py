#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utility to help us make a test case for release.

It does this by printing out the first new time for each APID. We may encounter
problems if segmented packets span multiple files, but that doesn't seem to be the case so far.

Copyright © 2014-2018 University of Wisconsin Regents

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
GNU General Public License for more details.
"""

from netCDF4 import Dataset

from sp_structs import parse_packet
from cache import datetime_from_hp

import argparse

import logging
LOG = logging.getLogger(__name__)

APID_TIMES = {}
global CURRENT_FILE


def print_new_times(netcdf_filelist):
    global CURRENT_FILE
    for f in netcdf_filelist:
        CURRENT_FILE = f
        nc = Dataset(CURRENT_FILE, 'r')
        packets = nc.variables['grb_space_packet_data'][:]
        pbuffer = packets.tobytes()
        _buffer2times(pbuffer)


def _buffer2times(pbuffer):
    start = 0
    while start < len(pbuffer):
        h1, h2, hp, _ = parse_packet(pbuffer, start)
        end = start + h1.data_length + 7
        try:
            date = datetime_from_hp(hp)
            apid = h1.apid
            _checktime(apid, date)
        except:
            date = None
        start = end


def _checktime(apid, time):
    if apid in APID_TIMES:
        if time != APID_TIMES[apid]:
            APID_TIMES[apid] = time
            _printtime(apid, time)
        else:
            return  # it matches, nothing to see here...
    else:
        APID_TIMES[apid] = time


def _printtime(apid, time):
    global CURRENT_FILE
    print(hex(apid), time, CURRENT_FILE)


def _setup_argparse():
    parser = argparse.ArgumentParser(description=__doc__)

    # Required arguments:
    parser.add_argument('input', nargs=argparse.REMAINDER,
                        help='any number of netcdf files, ideally in chronological order')

    return parser

if __name__ == '__main__':
    # Get input args
    parser = _setup_argparse()
    args = parser.parse_args()

    print_new_times(args.input)
