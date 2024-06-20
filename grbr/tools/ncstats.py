#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Print some basic netcdf stats about the variables contained in a file.

Copyright © 2017-2018 University of Wisconsin Regents

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

from netCDF4 import Dataset
import os

def ncstats(filename):
    ncf = Dataset(filename, 'r')
    for v in ncf.variables:
        print("Variable:", v)
        print("Chunking:", ncf.variables[v].chunking())
        print("Filters:", ncf.variables[v].filters())
        print("-------------------------------")


def _setup_argparse():
    import argparse
    parser = argparse.ArgumentParser(description="Print some basic netcdf stats about the variables contained in a file.")

    # Required arguments:
    parser.add_argument('files', nargs=argparse.REMAINDER, help='any number of NetCDF4 files')

    return parser

if __name__ == '__main__':
    # Get input args
    parser = _setup_argparse()
    args = parser.parse_args()

    # Process input
    for input in args.files:
        if os.path.exists(input):
            ncstats(input)
        else:
            print("File does not exist: %s" % input)
