#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utility to dump ccsds bundles out of DOE nc files.

Example usage: `python grb-r/nc2ccsds.py 15m.ccsds data/`

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

from datetime import datetime
import sys
import os
import numpy as np
from netCDF4 import Dataset
import ctypes

_, o, d = sys.argv

out = open(o, 'wb')

# 6 BYTES


class SP_PRIMARY_HEADER(ctypes.BigEndianStructure):
    _pack_ = 1
    _fields_ = [('packet_version_number', ctypes.c_uint8, 3),  # 0b000 for CCSDS Space Packet Version 1
                ('packet_type',           ctypes.c_uint8, 1),  # 0b0 for telemetry
                # do we have a secondary header?
                ('secondary_header_flag', ctypes.c_uint8, 1),
                # application process identifier - see APID_LOOKUP
                ('apid',                  ctypes.c_uint16, 11),
                # 0b00 middle, 0b01 first, 0b10 last, 0b11 unsegmented
                ('sequence_flags',        ctypes.c_uint8, 2),
                ('sequence_count',        ctypes.c_uint16, 14),  # mod 16384 counter
                # packet size in octets minus 7
                ('data_length',           ctypes.c_uint16, 16),
                ]

    def receiveSome(self, bytes):
        fit = min(len(bytes), ctypes.sizeof(self))
        ctypes.memmove(ctypes.addressof(self), bytes, fit)


# initialize the structure we will use to parse APIDs from the CCSDS
# packets before we send them
apid_checker = SP_PRIMARY_HEADER()
apid_checker.apid = 0

tstart = datetime.now()
print("Start at:", tstart)
f = os.listdir(d)
for nfile, ncfile in enumerate(sorted(f)):
    ncfile = os.path.join(d, ncfile)
    print(ncfile)
    nc = Dataset(ncfile, 'r')
    packets = nc.variables['grb_space_packet_data'][:]
    offsets = nc.variables['offset_to_packet'][:]
    sizes = nc.variables['size_of_packet'][:]

    for i in range(len(sizes)):
        s = sizes[i]
        o = offsets[i]
        p = packets[o:o + s]
        p = p.astype(np.int8).tostring()
        apid_checker.receiveSome(p)
        out.write(p)
    sys.stdout.write('\r')
    sys.stdout.write("Dumped %d of %d files..." % (nfile + 1, len(f)))
    sys.stdout.flush()

print("")
tend = datetime.now()
print("Done at:", tend)
print("Elapsed:", tend - tstart)
out.close()
