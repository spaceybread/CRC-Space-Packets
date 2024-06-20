#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module containing space packet, ccsds, grb, etc. structs

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

import ctypes

from grbr.apid import IMAGE, GENERIC
import logging
LOG = logging.getLogger('GRB-R')

SP_PRIMARY_HEADER_SIZE = 6
SP_SECONDARY_HEADER_SIZE = 8
SP_IMAGE_HEADER_SIZE = 34
SP_GENERIC_HEADER_SIZE = 21


class UsefulStruct(ctypes.BigEndianStructure):

    def send(self):
        return buffer(self)[:]

    def receiveSome(self, bytes):
        fit = min(len(bytes), ctypes.sizeof(self))
        ctypes.memmove(ctypes.addressof(self), bytes, fit)

# 6 BYTES


class SP_PRIMARY_HEADER(UsefulStruct):
    _pack_ = 1
    _fields_ = [('packet_version_number', ctypes.c_uint8, 3),  # 0b000 for CCSDS Space Packet Version 1
                ('packet_type',           ctypes.c_uint8, 1),  # 0b0 for telemetry
                # do we have a secondary header?
                ('secondary_header_flag', ctypes.c_uint8, 1),
                # application process identifier - see APID_LOOKUP
                ('apid',                  ctypes.c_uint16, 11),
                # 0b01 first, 0b10 last, 0b00 unseq
                ('sequence_flags',        ctypes.c_uint8, 2),
                ('sequence_count',        ctypes.c_uint16, 14),  # mod 16384 counter
                # packet size in octets minus 7
                ('data_length',           ctypes.c_uint16, 16),
                ]

# 8 BYTES


class SP_SECONDARY_HEADER(UsefulStruct):
    _pack_ = 1
    _fields_ = [('days_since_epoch',    ctypes.c_uint16, 16),  # days since jan 1 2000
                ('milliseconds_of_day', ctypes.c_uint32, 32),
                ('grb_version',         ctypes.c_uint16, 5),
                ('payload_variant',     ctypes.c_uint16, 5),
                ('assembler_id',        ctypes.c_uint16, 2),
                ('system_environment',  ctypes.c_uint16, 4),
                ]



class SP_IMAGE_HEADER(UsefulStruct):
    _pack_ = 1
    _fields_ = [('compression_algorithm',      ctypes.c_uint8, 8),
                ('seconds_since_epoch',        ctypes.c_uint32, 32),
                ('microseconds_of_second',     ctypes.c_uint32, 32),
                ('data_sequence_count',        ctypes.c_uint16, 16),
                # FIXME: 24 throws the size off, how do we do?
                ('row_offset',                 ctypes.c_uint16, 16),
                ('row_offsetB',                ctypes.c_uint8,  8),
                ('ul_x',                       ctypes.c_uint32, 32),
                ('ul_y',                       ctypes.c_uint32, 32),
                ('height',                     ctypes.c_uint32, 32),
                ('width',                      ctypes.c_uint32, 32),
                ('dqf_offset',                 ctypes.c_uint32, 32),
                ]


class SP_GENERIC_HEADER(UsefulStruct):
    _pack_ = 1
    _fields_ = [('compression_algorithm',      ctypes.c_uint8,  8),
                ('seconds_since_epoch',        ctypes.c_uint32, 32),
                ('microseconds_of_second',     ctypes.c_uint32, 32),
                ('reserved1',                  ctypes.c_uint64, 64),
                ('data_sequence_count',        ctypes.c_uint32, 32),
                ]

assert(ctypes.sizeof(SP_PRIMARY_HEADER) == SP_PRIMARY_HEADER_SIZE)
assert(ctypes.sizeof(SP_SECONDARY_HEADER) == SP_SECONDARY_HEADER_SIZE)
assert(ctypes.sizeof(SP_IMAGE_HEADER) == SP_IMAGE_HEADER_SIZE)
assert(ctypes.sizeof(SP_GENERIC_HEADER) == SP_GENERIC_HEADER_SIZE)


def _dump_struct(astruct):
    if astruct:
        for field_name, field_type, bitcount in astruct._fields_:
            attr = getattr(astruct, field_name)
            if field_name == "apid":
                attr = hex(attr)
            LOG.debug("%s: %s" % (field_name, attr))
