#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utility to monitor the GRB event log for new ABI datasets, find corresponding
tracking files, and generate basic plots for monitoring purposes.

Copyright © 2017-2018 University of Wisconsin Regents

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
GNU General Public License for more details.
"""

import argparse
import os

import numpy as np
from netCDF4 import Dataset

import logging
LOG = logging.getLogger(__name__)


ACTIVE_DATASETS = {}

def _setup_argparse():
    parser = argparse.ArgumentParser(description=__doc__)

    # Required arguments:
    parser.add_argument('eventlog', nargs=1,
                        help='the GRB event log to monitor and create plots from')

    # Optional arguments:
    # maybe an argument to specify what bands you care about?
    parser.add_argument('-v', '--verbose', dest='verbosity', action="count", default=0,
                        help='each occurrence increases verbosity through ERROR, WARNING, INFO, DEBUG')

    return parser


def tracking_file_handler(dataset, tracking_file, netcdf_file):
    """
    TRACKING FILE FORMAT
    <west bounds> <north bounds> <east bounds> <south bounds>
    aka
    <upper left x> <upper left y> <bottom right x> <bottom right y>
    """
    nc = Dataset(netcdf_file, 'r')
    vrad = nc.variables['Rad']
    data = np.zeros(vrad.shape) # FIXME: how do we handle fill value? change this to masked array maybe?

    with open(tracking_file) as f:
        ul_x, ul_y, br_x, br_y = f.readline().split()
        data[ul_y:br_y, ul_x:br_x] = vrad[ul_y:br_y, ul_x:br_x]



def eventlog_line_handler(line):
    """
    EVENT LOGGING FORMAT
    [%datetime] : %type of alert : %dataset : %dataset time : %file
    [2016-02-03 18:30:30.932239] : Dataset Start : GOES-16 ABI Band 1 Full Disk (Mode 3) : 2016-02-03 18:30:30.932239 : /tmp/where/this/file/is/ABI.nc
    """
    time, title, dataset_name, dataset_time, dataset_location = line.split(" : ")
    if title == "Dataset Start":
        tracking_file_handler(dataset_name, os.path.splitext(dataset_location)[0]+'.track', dataset_location)


def monitor(file_path):
    # https://stackoverflow.com/questions/36327265/python-parse-log-file-in-realtime-reload-when-the-log-rotates
    # is our launching point for following a rotating log file
    with open(file_path) as f:
        file_size = 0
        while True:
            line = f.readline()
            if line:
                eventlog_line_handler(line)
            file_status_obj = os.stat(file_path)
            if file_size < file_status_obj.st_size:
                f.seek(0)
            file_size = file_status_obj.st_size


def main():
    # Get input args
    parser = _setup_argparse()
    args = parser.parse_args()

    # Setup logging
    levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    verbosity = min(args.verbosity, len(levels) - 1)
    logging.basicConfig(level=levels[verbosity])

    monitor(args.eventlog)


if __name__ == '__main__':
    main()
