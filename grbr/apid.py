#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Various APID dictionaries, lookup tables, and a utility for printing a known APID table

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

IMAGE = 10001
GENERIC = 10002

DATA = 31459
METADATA = 26535

ABI = 9001
GLM = 9002
MAG = 9003
SEISS = 9004
EXIS = 9005
SUVI = 9006
INFO = 9007

apids = {}

#--- ABI ---

abi_names = [
    "ABI Full Disk Metadata (Mode 6)",
    "ABI Full Disk Radiance Image Data (Mode 6)",
    "ABI Continental United States Metadata (Mode 6)",
    "ABI Continental United States Radiance Image (Mode 6)",
    "ABI Mesoscale #1 Metadata (Mode 6)",
    "ABI Mesoscale #1 Radiance Image (Mode 6)",
    "ABI Mesoscale #2 Metadata (Mode 6)",
    "ABI Mesoscale #2 Radiance Image (Mode 6)",

    "ABI Full Disk Metadata (Mode 3)",
    "ABI Full Disk Radiance Image Data (Mode 3)",
    "ABI Continental United States Metadata (Mode 3)",
    "ABI Continental United States Radiance Image (Mode 3)",
    "ABI Mesoscale #1 Metadata (Mode 3)",
    "ABI Mesoscale #1 Radiance Image (Mode 3)",
    "ABI Mesoscale #2 Metadata (Mode 3)",
    "ABI Mesoscale #2 Radiance Image (Mode 3)",

    "ABI Full Disk Metadata (Mode 4)",
    "ABI Full Disk Radiance Image Data (Mode 4)",

    "ABI CONUS Metadata (Extracted from Full Disk Mode 4)",

    "ABI Non-Standard ABI Image Metadata",
    "ABI Non-Standard ABI Radiance Image Data",
]


abi_bands = range(1, 17)

abi_apid_base = 0x080

a = abi_apid_base
for name in abi_names:
    for band in abi_bands:
        apids[a] = name + " Band %02d" % (band)
        a += 1

#--- GLM ---

apids[0x300] = "GLM Lightning Detection Metadata"
apids[0x301] = "GLM Flash Data"
apids[0x302] = "GLM Group Data"
apids[0x303] = "GLM Event Data"


#--- EXIS ---

apids[0x380] = "EXIS Solar Flux: EUV Metadata"
apids[0x381] = "EXIS Solar Flux: EUV Data"
apids[0x382] = "EXIS Solar Flux: X-Ray Metadata"
apids[0x383] = "EXIS Solar Flux: X-Ray Data"

#--- SEISS ---

apids[0x400] = "SEISS Energetic Heavy Ions Metadata"
apids[0x401] = "SEISS Energetic Heavy Ions Data"
apids[0x410] = "SEISS Magnetospheric Electrons and Protons: Low Energy Metadata"
apids[0x411] = "SEISS Magnetospheric Electrons and Protons: Low Energy Data"
apids[0x420] = "SEISS Magnetospheric Electrons and Protons: Medium and High Energy Metadata"
apids[0x421] = "SEISS Magnetospheric Electrons and Protons: Medium and High Energy Data"
apids[0x430] = "SEISS Solar and Galactic Protons Metadata"
apids[0x431] = "SEISS Solar and Galactic Protons Data"

#--- SUVI ---

apids[0x480] = "SUVI Solar Imagery: X-Ray Metadata Band Fe094"
apids[0x481] = "SUVI Solar Imagery: X-Ray Metadata Band Fe132"
apids[0x482] = "SUVI Solar Imagery: X-Ray Metadata Band Fe171"
apids[0x483] = "SUVI Solar Imagery: X-Ray Metadata Band Fe195"
apids[0x484] = "SUVI Solar Imagery: X-Ray Metadata Band Fe284"
apids[0x485] = "SUVI Solar Imagery: X-Ray Metadata Band He304"
apids[0x486] = "SUVI Solar Imagery: X-Ray Data Band Fe094"
apids[0x487] = "SUVI Solar Imagery: X-Ray Data Band Fe132"
apids[0x488] = "SUVI Solar Imagery: X-Ray Data Band Fe171"
apids[0x489] = "SUVI Solar Imagery: X-Ray Data Band Fe195"
apids[0x48a] = "SUVI Solar Imagery: X-Ray Data Band Fe284"
apids[0x48b] = "SUVI Solar Imagery: X-Ray Data Band He304"

#--- MAG ---

apids[0x500] = "MAG Metadata"
apids[0x501] = "MAG Product Data"

#--- INFO ---
apids[0x580] = "GRB INFO"

#-----------


def isMetadata(apid):
    # ABI
    if   (apid >= 0x080 and apid <= 0x08f) or \
         (apid >= 0x0a0 and apid <= 0x0af) or \
         (apid >= 0x0c0 and apid <= 0x0cf) or \
         (apid >= 0x0e0 and apid <= 0x0ef) or \
         (apid >= 0x100 and apid <= 0x10f) or \
         (apid >= 0x120 and apid <= 0x12f) or \
         (apid >= 0x140 and apid <= 0x14f) or \
         (apid >= 0x160 and apid <= 0x16f) or \
         (apid >= 0x180 and apid <= 0x18f):
        return True
    # GLM
    elif (apid == 0x300):
        return True
    # EXIS
    elif (apid == 0x380 or apid == 0x382):
        return True
    # SEISS
    elif (apid == 0x400 or apid == 0x410 or apid == 0x420 or apid == 0x430):
        return True
    # SUVI
    elif (apid >= 0x480 and apid <= 0x485):
        return True
    # MAG
    elif (apid == 0x500):
        return True
    else:
        return False


def isData(apid):
    # ABI
    if   (apid >= 0x090 and apid <= 0x09f) or \
         (apid >= 0x0b0 and apid <= 0x0bf) or \
         (apid >= 0x0d0 and apid <= 0x0df) or \
         (apid >= 0x0f0 and apid <= 0x0ff) or \
         (apid >= 0x110 and apid <= 0x11f) or \
         (apid >= 0x130 and apid <= 0x13f) or \
         (apid >= 0x150 and apid <= 0x15f) or \
         (apid >= 0x170 and apid <= 0x17f) or \
         (apid >= 0x190 and apid <= 0x19f):
        return True
    # GLM
    elif (apid >= 0x301 and apid <= 0x303):
        return True
    # EXIS
    elif (apid >= 0x381 and apid <= 0x383):
        return True
    # SEISS
    elif (apid == 0x401 or apid == 0x411 or apid == 0x421 or apid == 0x431):
        return True
    # SUVI
    elif (apid >= 0x486 and apid <= 0x48b):
        return True
    # MAG
    elif (apid == 0x501):
        return True
    # INFO
    elif (apid == 0x580):
        return True
    else:
        return False



def apid2instr(apid):
    if apid >= 0x080 and apid <= 0x19f:
        return ABI
    elif apid >= 0x300 and apid <= 0x303:
        return GLM
    elif apid >= 0x380 and apid <= 0x383:
        return EXIS
    elif apid >= 0x400 and apid <= 0x431:
        return SEISS
    elif (apid >= 0x480 and apid <= 0x48b):
        return SUVI
    elif apid == 0x500 or apid == 0x501:
        return MAG
    elif apid == 0x580:
        return INFO
    else:
        return None


def pprint(dict):
    for key in sorted(dict.keys()):
        print("%x" % key, key, dict[key])

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='APID lookup')
    parser.add_argument('-d', action='store_true',
                        help='print the APID dictionary')
    parser.add_argument('-x', action='store_true',
                        help='denotes the APID is provided as hex')
    parser.add_argument('apid', type=str, nargs='?', default=None)
    args = parser.parse_args()

    if args.d:
        pprint(apids)
        exit()

    if args.apid is None:
        print("No apid provided, exiting.")
        parser.print_help()
        exit()

    if args.x:
        apid = int(args.apid, 16)
    else:
        apid = int(args.apid)

    if apid in apids.keys():
        print(apids[apid])
    else:
        print("ERROR: APID not recognized")
