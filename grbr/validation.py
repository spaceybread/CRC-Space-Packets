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

import os
import mmap
import argparse

#from parser import parse_packet

import logging
LOG = logging.getLogger('GRB-R')

ACCEPTED_VALUES = {}
ACCEPTED_VALUES['packet_version_number'] = [0b000]
ACCEPTED_VALUES['packet_type'] = [0b0]
ACCEPTED_VALUES['secondary_header_flag'] = [0b0, 0b1]
# ACCEPTED_VALUES['apid']
ACCEPTED_VALUES['sequence_flags'] = [0b00, 0b01, 0b10, 0b11]
#ACCEPTED_VALUES['sequence_count'] = modulo-16384
#ACCEPTED_VALUES['data_length'] > 0

# ACCEPTED_VALUES['days_since_epoch'] = > 0
# ACCEPTED_VALUES['milliseconds_of_day'] = > 0
ACCEPTED_VALUES['grb_version'] = [0b000]
ACCEPTED_VALUES['payload_variant'] = [0, 2, 3]  # 1 is reserved
ACCEPTED_VALUES['assembler_id'] = [0, 1, 2, 3]
ACCEPTED_VALUES['system_environment'] = [0, 1, 2]

ACCEPTED_VALUES['compression_algorithm'] = [0, 1, 2]
# ACCEPTED_VALUES['seconds_since_epoch'] = > 0
# ACCEPTED_VALUES['microseconds_of_second'] = > 0
# ??? are there any simple checks for these?
# ACCEPTED_VALUES['sequence_count']
# ACCEPTED_VALUES['row_offset']
# ACCEPTED_VALUES['row_offsetB']
# ACCEPTED_VALUES['ul_x']
# ACCEPTED_VALUES['ul_y']
# ACCEPTED_VALUES['height']
# ACCEPTED_VALUES['width']
# ???
# ACCEPTED_VALUES['dqf_offset'] = < length(payload)


def validate_gt(packet, name, threshold=0):
    value = getattr(packet, name)
    if not value > threshold:
        LOG.warning("Invalid (<= %s) %s: %s", str(threshold), name, str(value))
        return 1
    return 0


def validate_lt(packet, name, threshold):
    value = getattr(packet, name)
    if not value < threshold:
        LOG.warning("Invalid (>= %s) %s: %s", str(threshold), name, value)
        return 1
    return 0


def validate_compare(packet, name):
    value = getattr(packet, name)
    if value not in ACCEPTED_VALUES[name]:
        LOG.warning("Unrecognized %s: %s", name, str(value))
        return 1
    return 0


def validate_h1(h1):
    e = 0
    e += validate_compare(h1, 'packet_version_number')
    e += validate_compare(h1, 'packet_type')
    e += validate_compare(h1, 'secondary_header_flag')
    e += validate_compare(h1, 'sequence_flags')
    e += validate_gt(h1, 'data_length')
    return e


def validate_h2(h2):
    e = 0
    e += validate_compare(h2, 'grb_version')
    e += validate_compare(h2, 'payload_variant')
    e += validate_compare(h2, 'assembler_id')
    e += validate_compare(h2, 'system_environment')
    e += validate_gt(h2, 'days_since_epoch')
    e += validate_gt(h2, 'milliseconds_of_day')
    return e


def validate_hp(hp):
    e = 0
    e += validate_compare(hp, 'compression_algorithm')
    e += validate_gt(hp, 'seconds_since_epoch', -1)
    e += validate_gt(hp, 'microseconds_of_second', -1)
    return e

# def validate_gen(hp):
#  e = 0
#  e += validate_compare(hp, 'compression_algorithm')
#  e += validate_gt(hp, 'seconds_since_epoch')
#  e += validate_gt(hp, 'microseconds_of_second')
#  return e
#
# def validate_img(hp):
#  e = 0
#  e += validate_compare(hp, 'compression_algorithm')
#  e += validate_gt(hp, 'seconds_since_epoch')
#  e += validate_gt(hp, 'microseconds_of_second')
#  return e


def validate(h1, h2, hp):
    e = 0
    if h1 is not None:
        e += validate_h1(h1)
    if h2 is not None:
        e += validate_h2(h2)
    if hp is not None:
        e += validate_hp(hp)
    return e