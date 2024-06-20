#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Grabbing environment variables and other needed-everywhere constants

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

from os import getenv, getcwd, path

# commonly reconfigured values
CSPP_GEO_GRB_HOME = getenv("CSPP_GEO_GRB_HOME", getcwd())

CSPP_GEO_GRB_OUT = getenv("CSPP_GEO_GRB_OUT", getcwd())
CSPP_GEO_GRB_LOG = getenv("CSPP_GEO_GRB_LOG", path.join(CSPP_GEO_GRB_OUT, "log"))

CSPP_GEO_GRBR_TMP = path.join(getenv("CSPP_GEO_GRB_TMP", path.join(CSPP_GEO_GRB_OUT, "tmp")), "GRB-R")
CSPP_GEO_GRBR_OUT = getenv("CSPP_GEO_GRB_PRODUCT", path.join(CSPP_GEO_GRB_OUT, "product"))
CSPP_GEO_GRBR_TRACK = getenv("CSPP_GEO_GRB_TRACK", path.join(CSPP_GEO_GRB_OUT, "track"))

CSPP_GEO_GRB_POST_PROCESS_SCRIPT = getenv("CSPP_GEO_GRB_POST_PROCESS_SCRIPT", "")

# "power user" type tweaks
CSPP_GEO_GRBR_SZIP_LIB = getenv("CSPP_GEO_GRBR_SZIP_LIB", CSPP_GEO_GRB_HOME + "/deps/libsz.so")

CSPP_GEO_GRBR_DEBUG = int(getenv("CSPP_GEO_GRBR_DEBUG", 0))

CSPP_GEO_GRBR_TIMEOUT = int(getenv("CSPP_GEO_GRBR_TIMEOUT", 1800))  # timeout after 30 min of no new data

CSPP_GEO_GRBR_SATELLITE_KEY = getenv("CSPP_GEO_GRBR_SATELLITE_KEY", "")

CSPP_GEO_GRBR_ENABLE_VALIDATION = int(getenv("CSPP_GEO_GRBR_ENABLE_VALIDATION", 1)) # if you don't care about validation, this flag lets you skip it for performance

CSPP_GEO_GRBR_TOSS_FAILED_VALIDATION = int(getenv("CSPP_GEO_GRBR_TOSS_FAILED_VALIDATION", 0)) # whether to toss a packet or just log when the validation check fails

CSPP_GEO_GRBR_ENABLE_CRC_CHECKS = int(getenv("CSPP_GEO_GRBR_ENABLE_CRC_CHECKS", 1)) # if you don't care about crc checks, this flag lets you skip it for performance

CSPP_GEO_GRBR_TOSS_FAILED_CRC = int(getenv("CSPP_GEO_GRBR_TOSS_FAILED_CRC", 0)) # whether to toss a packet or just log when the crc check fails

CSPP_GEO_GRBR_ENABLE_TRACKING = int(getenv("CSPP_GEO_GRBR_ENABLE_TRACKING", 0)) # don't write tracking files unless they're going to be used

CSPP_GEO_GRBR_ENABLE_EVENT_LOG = bool(int(getenv("CSPP_GEO_GRBR_ENABLE_EVENT_LOG", 0))) # don't write an event log unless it's going to be used

CSPP_GEO_GRBR_EVENT_LOG_PATH = getenv("CSPP_GEO_GRBR_EVENT_LOG_PATH", path.join(CSPP_GEO_GRB_LOG, "event/grb-events.log"))

CSPP_GEO_GRBR_EVENT_LOG_FILES_TO_KEEP = int(getenv("CSPP_GEO_GRBR_EVENT_LOG_FILES_TO_KEEP", 5))

CSPP_GEO_GRBR_EVENT_LOG_ROTATE_EVERY = int(getenv("CSPP_GEO_GRBR_EVENT_LOG_ROTATE_EVERY", 512*1024)) # in bytes

CSPP_GEO_GRBR_DEFAULT_COMPRESSION = int(getenv("CSPP_GEO_GRBR_DEFAULT_COMPRESSION", 1))

CSPP_GEO_GRBR_IMAGE_COMPRESSION = int(getenv("CSPP_GEO_GRBR_IMAGE_COMPRESSION", CSPP_GEO_GRBR_DEFAULT_COMPRESSION))

def _get_version():
    try:
        version_filename = path.join(CSPP_GEO_GRB_HOME, "VERSION.txt")
        return open(version_filename, 'r').read().rstrip()
    except:
        return "unknown"

VERSION = _get_version()