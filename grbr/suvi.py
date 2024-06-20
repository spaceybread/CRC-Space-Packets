#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Various SUVI dictionaries, lookup tables, and etc.

Copyright © 2014-2018 University of Wisconsin Regents

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTSUVILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

from grbr.dataset import GRBDataset
from grbr.config import CSPP_GEO_GRBR_ENABLE_TRACKING, CSPP_GEO_GRBR_IMAGE_COMPRESSION
import numpy as np

import os
import logging
LOG = logging.getLogger('GRB-R')


def band(apid):
    # FIXME: look into how these bands should actually be labeled?
    return (apid % 8) + 1


class SUVI(GRBDataset):
    track = True

    def __init__(self, h1, h2, hp):
        super(SUVI, self).__init__(h1, h2, hp)
        os.putenv("OPJ_FORCE_SGND", "1")
        self.size = self._get_size()
        self.bit_depth = self._get_depth()         # example for 16b
        self.fill = pow(2, self.bit_depth - 1) * -1  # -32768
        self.bit_mask = pow(2, self.bit_depth) - 1   # 65535
        self.pixels_seen = 0
        self._init_netcdf()

    def _init_netcdf(self):
        self.nc.set_fill_on()
        self.nc.createDimension('NAXIS2', self.size[0])
        self.nc.createVariable('NAXIS2', 'i2', ('NAXIS2',), zlib=True, complevel=CSPP_GEO_GRBR_IMAGE_COMPRESSION)
        self.nc.variables["NAXIS2"][:] = range(self.size[0])
        self.nc.createDimension('NAXIS1', self.size[1])
        self.nc.createVariable('NAXIS1', 'i2', ('NAXIS1',), zlib=True, complevel=CSPP_GEO_GRBR_IMAGE_COMPRESSION)
        self.nc.variables["NAXIS1"][:] = range(self.size[1])
        self.ncrad = self.nc.createVariable(
            'RAD', 'i2', ('NAXIS2', 'NAXIS1'), fill_value=self.fill, zlib=True, complevel=CSPP_GEO_GRBR_IMAGE_COMPRESSION)
        self.ncrad.set_auto_maskandscale(False)
        self.ncdqf = self.nc.createVariable(
            'DQF', 'u1', ('NAXIS2', 'NAXIS1'), fill_value=255, zlib=True, complevel=CSPP_GEO_GRBR_IMAGE_COMPRESSION)
        self.ncdqf.set_auto_maskandscale(False)
        self.nc.sync()

    def _add_data(self, h1, h2, hp, p):
        LOG.info("Adding data payload...")
        try:
            rad = self._decompress(hp, p[:hp.dqf_offset])
        except:
            LOG.error("Error decompressing Rad, dropping fragment...")
            return
        try:
            dqf = self._decompress(hp, p[hp.dqf_offset:])
        except:
            LOG.error("Error decompressing DQF, dropping fragment...")
            return

        rad = rad.astype(np.int16)
        dqf = dqf.astype(np.int8)

        ul_x, ul_y, br_x, br_y = self._ulbr(hp, rad.shape)
        self.ncrad[ul_y:br_y, ul_x:br_x] = rad
        self.ncdqf[ul_y:br_y, ul_x:br_x] = dqf

        self.track(ul_x, ul_y, br_x, br_y)
        self.nc.sync()

        self.pixels_seen += (rad.shape[0] * rad.shape[1])
        LOG.debug("Done adding data...")


    def track(self, ul_x, ul_y, br_x, br_y):
        if CSPP_GEO_GRBR_ENABLE_TRACKING:
            self.tracking_file.write("%d %d %d %d\n" % (ul_x, ul_y, br_x, br_y))

    def _ulbr(self, hp, shape):
        # note SUVI appears to be reversed? lower instead of upper in header?
        h, w = shape
        ul_x, ul_y = (hp.ul_x, hp.ul_y)
        # FIXME: handling for 24-bit, see struct
        row_offset = (hp.row_offset << 8) + hp.row_offsetB
        ul_y = ul_y + row_offset
        br_x = ul_x + w
        br_y = ul_y + h
        return ul_x, ul_y, br_x, br_y

    def _get_size(self):
        return (1280, 1280)

    def _get_depth(self):
        return 16  # FIXME: seeing conflicting information about whether this should be 16 or 14
