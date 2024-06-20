#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Various functions to parse out CCSDS packet headers and payloads from
various GRB stream containers.

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

from grbr.sp_structs import SP_PRIMARY_HEADER, SP_SECONDARY_HEADER, SP_IMAGE_HEADER, SP_GENERIC_HEADER
from grbr.sp_structs import SP_PRIMARY_HEADER_SIZE, SP_SECONDARY_HEADER_SIZE, SP_IMAGE_HEADER_SIZE, SP_GENERIC_HEADER_SIZE
from grbr.sp_structs import _dump_struct
from grbr.validation import validate
from grbr.apid import IMAGE, GENERIC
from grbr.config import CSPP_GEO_GRBR_ENABLE_VALIDATION
from grbr.config import CSPP_GEO_GRBR_ENABLE_CRC_CHECKS
import traceback
import zlib

import logging
LOG = logging.getLogger('GRB-R')

from time import perf_counter as pc
# 3141 - Checking performance


def parse_bundle_file(file, safe_validation=False, safe_crc=False, quiet=False):
    """
    Generator for a packet bundle file that yields h1, h2, hp, p.
    """
    offset = 0
    while True:  # FIXME: is this the best way to end?
        LOG.debug("Parsing bundle at offset [%d]" % (offset))
        try:
            h1, h2, hp, p, length = parse_bundle(file, offset, safe_validation=safe_validation, safe_crc=safe_crc, quiet=quiet)
        except Exception as e:
            LOG.error("Parsing bundle file failed at offset [%d]:" % (offset))
            LOG.error(traceback.print_exc())
            return
        yield h1, h2, hp, p, length
        offset += length
        LOG.debug("Next bundle offset: [%d]" % (offset))



def parse_bundle(file, offset, safe_validation=False, safe_crc=False, quiet=False):
    """
    Parse a full packet bundle.
    """
    h1 = h2 = hp = p = None
    length = 0

    h1, h2, hp, p = parse_packet(file, offset, safe_validation=safe_validation, safe_crc=safe_crc, quiet=quiet)
    length = h1.data_length + 7

    # we have an incomplete packet, build the rest...
    if h1.sequence_flags == 0b00 or h1.sequence_flags == 0b01:
        count = h1.sequence_count
        _h1 = h1
        # FIXME: not a fan of this while-true loop
        while True:
            offset += _h1.data_length + 7  # skip to the next packet
            LOG.debug("Incomplete payload, adding packet @ offset: %d", offset)
            _h1, _h2, _, _p = parse_packet(file, offset, safe_validation=safe_validation, safe_crc=safe_crc, quiet=quiet)
            if _h1.apid != h1.apid:
                LOG.error("APID mismatch [%s != %s], chucking a partial bundle." % (
                    hex(_h1.apid), hex(h1.apid)))
                raise(RuntimeError, "APID mismatch.")
            count = (count + 1) % 16384
            if _h1.sequence_count != count:
                LOG.error("Sequence counter out of order (got %05d, expected %05d); chucking these packets." % (
                    _h1.sequence_count, count))
#                raise(RuntimeError, "Sequence counter out of order.")
            length += _h1.data_length + 7
            p += _p
            if _h1.sequence_flags == 0b10:  # we hit the last packet in the sequence
                break
    return h1, h2, hp, p, length


def parse_packet(file, file_offset, safe_validation=False, safe_crc=False, quiet=False):
    """
    Takes a file object and offset, returns (primary, secondary, and payload) headers
    and the payload
    """
    h1 = h2 = hp = p = None

    # we need to parse the primary header to get the length of the packet
    h1 = SP_PRIMARY_HEADER()
    h1.receiveSome(_saferead(file, file_offset, SP_PRIMARY_HEADER_SIZE))
    if not quiet:
        LOG.debug("* h1:")
        _dump_struct(h1)

    # read the entire packet in one go to use later
    packet_size = h1.data_length + 7

#    print "📎", file_offset, packet_size, file_offset + packet_size
    packet = _saferead(file, file_offset, packet_size)

# this isn't necessary if we get _saferead to work
#    if len(packet) < packet_size:
#        LOG.error("WHY IS THIS PACKET SO MUCH SMALLER THAN PACKET SIZE??? %d" % (file_offset))

    packet_offset = SP_PRIMARY_HEADER_SIZE

    if h1.secondary_header_flag == 1:
        h2 = SP_SECONDARY_HEADER()
        h2.receiveSome(packet[packet_offset : packet_offset + SP_SECONDARY_HEADER_SIZE])
        packet_offset += SP_SECONDARY_HEADER_SIZE
        if not quiet:
            LOG.debug("* h2:")
            _dump_struct(h2)

    # we only have a payload header for the first section
    if h1.sequence_flags == 0b01 or h1.sequence_flags == 0b11:
        if h2.payload_variant == 2 or h2.payload_variant == 3:
            hp = SP_IMAGE_HEADER()
            hp.receiveSome(packet[packet_offset : packet_offset + SP_IMAGE_HEADER_SIZE])
            packet_offset += SP_IMAGE_HEADER_SIZE
        elif h2.payload_variant == 0:
            hp = SP_GENERIC_HEADER()
            hp.receiveSome(packet[packet_offset : packet_offset + SP_GENERIC_HEADER_SIZE])
            packet_offset += SP_GENERIC_HEADER_SIZE
        else:
            if not quiet:
                LOG.warning("Unrecognized payload type, APID: %s" % (h1.apid))
                LOG.warning("Payload variant: %s" % (h2.payload_variant))
        if not quiet:
            LOG.debug("* hp:")
            _dump_struct(hp)


    # 3141 - CRC check testing 2024-06-20
    LOG.info("// 3141 - CRC should start here // " * 4)
    start = pc()
    
    if CSPP_GEO_GRBR_ENABLE_CRC_CHECKS:
        LOG.debug("// 3141 - CRC check is enabled // " * 4)
        crc_start = packet_size - 4
        p = packet[packet_offset : crc_start]

        crc_zone = packet[0 : crc_start]
        crc = packet[crc_start : crc_start + 4]
        if len(crc) == 0:
            raise(RuntimeError, "CRC field is empty; did we go off the end of the file?")
        crc = int(crc.hex(), 16)

        crc_calculated = zlib.crc32(crc_zone) & 0xffffffff
        if crc != crc_calculated:
            LOG.error("Packet failed the CRC check.")
            if safe_crc:
                raise(RuntimeError, "Packet failed the CRC check.")

    LOG.info("CRC check done in: ", pc() - start, "seconds")
            
    if CSPP_GEO_GRBR_ENABLE_VALIDATION and validate(h1, h2, hp) > 0:
        LOG.error("Packet failed validation.")
        if safe_validation:
            raise(RuntimeError, "Packet failed validation.")

    return h1, h2, hp, p


def _get_f_size(f):
    f.seek(0, 2)
    return f.tell()

from time import sleep
def _saferead(f, offset, length):
    while _get_f_size(f) < (offset + length):
        sleep(5)
    f.seek(offset)
    return f.read(length)
