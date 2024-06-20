#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Global event logging.

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

from grbr.config import CSPP_GEO_GRBR_EVENT_LOG_PATH
from grbr.config import CSPP_GEO_GRBR_ENABLE_EVENT_LOG
from grbr.config import CSPP_GEO_GRBR_EVENT_LOG_ROTATE_EVERY
from grbr.config import CSPP_GEO_GRBR_EVENT_LOG_FILES_TO_KEEP
# https://pypi.python.org/pypi/ConcurrentLogHandler/0.9.1
from logging import getLogger, INFO
from concurrent_log_handler import ConcurrentRotatingFileHandler
import os

if CSPP_GEO_GRBR_ENABLE_EVENT_LOG:
    log = getLogger('GRB-R Events')
    # Use an absolute path to prevent file rotation trouble.
    logfile = os.path.abspath(CSPP_GEO_GRBR_EVENT_LOG_PATH)

    # Rotate log after reaching 512K, keep 5 old copies.
    rotateHandler = ConcurrentRotatingFileHandler(logfile, "a", CSPP_GEO_GRBR_EVENT_LOG_ROTATE_EVERY, CSPP_GEO_GRBR_EVENT_LOG_FILES_TO_KEEP)
    log.addHandler(rotateHandler)
    log.setLevel(INFO)


# EVENT LOGGING FORMAT
# [%datetime] : %type of alert : %dataset : %dataset time : %file
# [2016-02-03 18:30:30.932239] : Dataset Start : GOES-16 ABI Band 1 Full Disk (Mode 3) : 2016-02-03 18:30:30.932239 : /tmp/where/this/file/is/ABI.hdf


def log_start(dataset_name, dataset_time, dataset_location):
    log_event("Dataset Start", dataset_name, dataset_time, dataset_location)


def log_end(dataset_name, dataset_time, dataset_location):
    log_event("Dataset End", dataset_name, dataset_time, dataset_location)

def log_error(dataset_name, dataset_time, dataset_location):
    log_event("Dataset Encountered Unrecoverable Error", dataset_name, dataset_time, dataset_location)

def log_timeout(dataset_name, dataset_time, dataset_location):
    log_event("Dataset Timed Out", dataset_name, dataset_time, dataset_location)

def _event_time_fmt(a_datetime):
    return a_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")

# Datasets only have one digit of partial second precision, and it's not particularly
# relevant for this purpose. There are no datasets that repeat within 1 second.
def _dataset_time_fmt(a_datetime):
    return a_datetime.strftime("%Y-%m-%d %H:%M:%S")

def log_event(event_title, dataset_name, dataset_time, dataset_location):
    if not CSPP_GEO_GRBR_ENABLE_EVENT_LOG:
        return
    now = datetime.now()
    msg = "[%s] : %s : %s : %s : %s" % (
        _event_time_fmt(now), event_title, dataset_name, _dataset_time_fmt(dataset_time), dataset_location)
    log.info(msg)
