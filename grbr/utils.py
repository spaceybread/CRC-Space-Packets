#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A catch-all spot for utility functions.

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

import os
import pwd
import sys
from datetime import datetime

def generate_history_string():
    """
    A global attribute for an audit trail. This is a character array with a line
    for each invocation of a program that has modified the dataset. Well-behaved
    generic netCDF applications should append a line containing: date, time of
    day,user name, program name and command arguments. 
    """
    items = {}
    d = datetime.utcnow()
    items['date'] = d.strftime("%Y-%m-%d")
    items['tod'] = d.strftime("%H:%M:%S")
    items['user'] = pwd.getpwuid(os.getuid())[0]
    items['args'] = " ".join(sys.argv)
    return "%(date)s, %(tod)s, %(user)s, %(args)s" % items