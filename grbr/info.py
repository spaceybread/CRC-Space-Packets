#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A generic dataset object for all of our GRB datasets to extend.

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

from grbr.cache import datetime_from_hp
from grbr.config import CSPP_GEO_GRBR_OUT
import grbr.apid
from grbr.eventlog import log_start, log_end

import os
import ctypes

from grbr.dataset import GRBDataset

import logging
LOG = logging.getLogger('GRB-R')


class GRBStruct(ctypes.LittleEndianStructure):

    def receiveSome(self, bytes):
        fit = min(len(bytes), ctypes.sizeof(self))
        ctypes.memmove(ctypes.addressof(self), bytes, fit)


def _dump_struct(astruct):
    for field_name, field_type in astruct._fields_:
        LOG.debug("%s: %s" % (field_name, getattr(astruct, field_name)))


class INFO(GRBDataset):
    track = False

    def __init__(self, h1, h2, hp):
        self.product_time = datetime_from_hp(hp)
        self.product_name = grbr.apid.apids[h1.apid]
        pass

    def add_bundle(self, h1, h2, hp, p):
        if grbr.apid.isMetadata(h1.apid):
            raise(NotImplementedError, "we don't expect to get metadata for INFO (apid: %s)" % hex(h1.apid))
        elif grbr.apid.isData(h1.apid):
            self._add_data(h1, h2, hp, p)
        else:
            raise(NotImplementedError, "APID %s is not recognized!" % hex(h1.apid))

        if self.finished():
            self.finalize()

    def _add_data(self, h1, h2, hp, p):
        LOG.info("Adding data payload...")
        try:
            payload = self._decompress(hp, p)
        except:
            LOG.error("Error decompressing xml, dropping info payload...")
            return

        id_size = ord(payload[0])
        # 16 + 104 + 24 + 128 + 32 = 304 appear to be our two sizes (in bytes)
        # 16 + 112 + 24 + 128 + 32 = 312

        identifier = payload[1:id_size + 1]
        filename = os.path.join(CSPP_GEO_GRBR_OUT, identifier)

        log_start(self.product_name, self.product_time, filename)

        xml = open(filename, 'w')
        xml.write(payload[id_size + 1:])
        xml.close()

        log_end(self.product_name, self.product_time, filename)

    def finished(self):
        return True

    def finalize(self):
        exit(0)
