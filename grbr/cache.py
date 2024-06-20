#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Basic cache utility functions

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

from datetime import datetime, timedelta
from grbr.config import CSPP_GEO_GRBR_SATELLITE_KEY
import grbr.apid as apid

import logging
LOG = logging.getLogger('GRB-R')


def abi_stub(h1, h2, hp):
    b = (h1.apid % 16) + 1

    # Add region & mode FIXME: how do we get spacecraft ID?
    if h1.apid >= 0x100 and h1.apid <= 0x11f:
        stub = "ABI-L1b-RadF-M3C%02d" % (b)
    elif h1.apid >= 0x120 and h1.apid <= 0x13f:
        stub = "ABI-L1b-RadC-M3C%02d" % (b)
    elif h1.apid >= 0x140 and h1.apid <= 0x15f:
        stub = "ABI-L1b-RadM1-M3C%02d" % (b)
    elif h1.apid >= 0x160 and h1.apid <= 0x17f:
        stub = "ABI-L1b-RadM2-M3C%02d" % (b)
    elif h1.apid >= 0x180 and h1.apid <= 0x19f:
        stub = "ABI-L1b-RadF-M4C%02d" % (b)
    elif h1.apid >= 0x080 and h1.apid <= 0x09f:
        stub = "ABI-L1b-RadF-M6C%02d" % (b)
    elif h1.apid >= 0x0a0 and h1.apid <= 0x0bf:
        stub = "ABI-L1b-RadC-M6C%02d" % (b)
    elif h1.apid >= 0x0c0 and h1.apid <= 0x0df:
        stub = "ABI-L1b-RadM1-M6C%02d" % (b)
    elif h1.apid >= 0x0e0 and h1.apid <= 0x0ff:
        stub = "ABI-L1b-RadM2-M6C%02d" % (b)
    else:
        raise(NotImplementedError)

    return stub


def glm_stub(h1, h2, hp):
    stub = "GLM"  # FIXME: look at metadata to see what this stub should be
    return stub


def mag_stub(h1, h2, hp):
    stub = "MAG"  # FIXME: look at metadata to see what this stub should be
    return stub


def seiss_stub(h1, h2, hp):
    if h1.apid in [0x400, 0x401]:
        return "SEISS-EHIS"
    elif h1.apid in [0x410, 0x411]:
        return "SEISS-MPSL"
    elif h1.apid in [0x420, 0x421]:
        return "SEISS-MPSH"
    elif h1.apid in [0x430, 0x431]:
        return "SEISS-SGPS"
    else:
        raise(NotImplementedError)


def exis_stub(h1, h2, hp):
    if h1.apid in [0x380, 0x381]:
        return "EXIS-EUV"
    elif h1.apid in [0x382, 0x383]:
        return "EXIS-XRAY"
    else:
        raise(NotImplementedError)


def suvi_stub(h1, h2, hp):
    if h1.apid in [0x480, 0x486]:
        return "SUVI-Fe094"
    elif h1.apid in [0x481, 0x487]:
        return "SUVI-Fe132"
    elif h1.apid in [0x482, 0x488]:
        return "SUVI-Fe171"
    elif h1.apid in [0x483, 0x489]:
        return "SUVI-Fe195"
    elif h1.apid in [0x484, 0x48A]:
        return "SUVI-Fe284"
    elif h1.apid in [0x485, 0x48B]:
        return "SUVI-He304"
    else:
        raise(NotImplementedError)


def info_stub(h1, h2, hp):
    if h1.apid in [0x580]:
        return "GRB-INFO"
    else:
        raise(NotImplementedError)

# note that we intentionally don't worry about leap seconds in this functions
# that's probably OK, as it's used for creating tmpnames and creating unique
# times between datasets (which shouldn't be separated by mere seconds)
# if this changes, we can add leap second support later


def datetime_from_hp(hp):
    epoch = datetime(2000, 1, 1, 12, 00, 00)
    if hp.seconds_since_epoch == 0 and hp.microseconds_of_second == 0:
        LOG.error(
            "Packet header seconds_since_epoch and microseconds_of_second are 0")
    tdiff = timedelta(days=0, seconds=hp.seconds_since_epoch,
                      microseconds=hp.microseconds_of_second)
    ptime = epoch + tdiff  # FIXME: we probably have to handle leap seconds here
    return ptime


def product_tmpname(h1, h2, hp):
    instr = apid.apid2instr(h1.apid)
    instr2stub = {apid.ABI: abi_stub,
                  apid.GLM: glm_stub,
                  apid.MAG: mag_stub,
                  apid.SEISS: seiss_stub,
                  apid.EXIS: exis_stub,
                  apid.SUVI: suvi_stub,
                  apid.INFO: info_stub,
                  }

    if instr in instr2stub:
        get_stub = instr2stub[instr]
    else:
        return "SPARE"

    stub = get_stub(h1, h2, hp)

    if CSPP_GEO_GRBR_SATELLITE_KEY != "":
        stub = stub + "_" + CSPP_GEO_GRBR_SATELLITE_KEY + "_"
    else:
        stub += "_" # we removed G16 here because we can't tell the difference between it and G17

    ptime = datetime_from_hp(hp)
    stub += ptime.strftime("s%Y%j%H%M%S")
    return stub
