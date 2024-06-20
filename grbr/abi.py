#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Various ABI dictionaries, lookup tables, and etc.

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

from grbr.config import CSPP_GEO_GRBR_ENABLE_TRACKING, CSPP_GEO_GRBR_IMAGE_COMPRESSION

from collections import namedtuple

from grbr.dataset import GRBDataset

import logging
LOG = logging.getLogger('GRB-R')

# from Table 7.1.3.1
ABI_Band = namedtuple('ABI_Band', 'band_num wavelength km bit_depth chunk_size')
ABI_Bands = {}
ABI_Bands[1] = ABI_Band(1,   0.47,    1,   10, (226,226))
ABI_Bands[2] = ABI_Band(2,   0.64,  0.5,   12, (226,226))
ABI_Bands[3] = ABI_Band(3,   0.865,   1,   10, (226,226))
ABI_Bands[4] = ABI_Band(4,   1.378,   2,   11, (226,226))
ABI_Bands[5] = ABI_Band(5,   1.61,    1,   10, (226,226))
ABI_Bands[6] = ABI_Band(6,   2.25,    2,   10, (226,226))
ABI_Bands[7] = ABI_Band(7,   3.9,     2,   14, (226,226))
ABI_Bands[8] = ABI_Band(8,   6.185,   2,   12, (226,226))
ABI_Bands[9] = ABI_Band(9,   6.95,    2,   11, (226,226))
ABI_Bands[10] = ABI_Band(10, 7.34,    2,   12, (226,226))
ABI_Bands[11] = ABI_Band(11, 8.5,     2,   12, (226,226))
ABI_Bands[12] = ABI_Band(12, 9.61,    2,   11, (226,226))
ABI_Bands[13] = ABI_Band(13, 10.35,   2,   12, (226,226))
ABI_Bands[14] = ABI_Band(14, 11.2,    2,   12, (226,226))
ABI_Bands[15] = ABI_Band(15, 12.3,    2,   12, (226,226))
ABI_Bands[16] = ABI_Band(16, 13.3,    2,   10, (226,226))

# from Table 7.1.2.6
ABI_Resolutions = {}
ABI_Resolutions['full disk'] = {}
ABI_Resolutions['full disk'][0.5] = (21696, 21696)
ABI_Resolutions['full disk'][1] = (10848, 10848)
ABI_Resolutions['full disk'][2] = (5424, 5424)
ABI_Resolutions['full disk'][4] = (2712, 2712)
ABI_Resolutions['full disk'][10] = (1086, 1086)
ABI_Resolutions['conus extraction'] = {}
ABI_Resolutions['conus extraction'][0.5] = (6000, 10000)
ABI_Resolutions['conus extraction'][1] = (3000, 5000)
ABI_Resolutions['conus extraction'][2] = (1500, 2500)
# ABI_Resolutions['conus extraction'][4]   = (,)
ABI_Resolutions['conus extraction'][10] = (301, 501)
ABI_Resolutions['conus'] = {}
ABI_Resolutions['conus'][0.5] = (6000, 10000)
ABI_Resolutions['conus'][1] = (3000, 5000)
ABI_Resolutions['conus'][2] = (1500, 2500)
# ABI_Resolutions['conus'][4]   = (,)
ABI_Resolutions['conus'][10] = (300, 500)
ABI_Resolutions['mesoscale'] = {}
ABI_Resolutions['mesoscale'][0.5] = (2000, 2000)
ABI_Resolutions['mesoscale'][1] = (1000, 1000)
ABI_Resolutions['mesoscale'][2] = (500, 500)
ABI_Resolutions['mesoscale'][4] = (250, 250)
ABI_Resolutions['mesoscale'][10] = (100, 100)


def apid2region(apid):
    # MODE 3
    if apid >= 0x100 and apid <= 0x11f:
        return "full disk"
    elif apid >= 0x120 and apid <= 0x13f:
        return "conus"
    elif apid >= 0x140 and apid <= 0x15f:
        return "mesoscale"
    elif apid >= 0x160 and apid <= 0x17f:
        return "mesoscale"
    # MODE 4
    elif apid >= 0x180 and apid <= 0x19f:
        return "full disk"
    # MODE 6
    elif apid >= 0x080 and apid <= 0x09f:
        return "full disk"
    elif apid >= 0x0a0 and apid <= 0x0bf:
        return "conus"
    elif apid >= 0x0c0 and apid <= 0x0df:
        return "mesoscale"
    elif apid >= 0x0e0 and apid <= 0x0ff:
        return "mesoscale"
    else:
        raise(NotImplementedError)


def band(apid):
    return (apid % 16) + 1


class ABI(GRBDataset):
    track = True

    def __init__(self, h1, h2, hp):
        super(ABI, self).__init__(h1, h2, hp)
        self.apid = h1.apid
        self.size = self._get_size()
        self.band = band(self.apid)
        self.bit_depth = self._get_depth()         # example for 16b
        self.bit_mask = pow(2, self.bit_depth) - 1   # 65535
        # ABI fill is all positive values at the top of the bit depth range
        self.fill = self.bit_mask
        self.pixels_seen = 0
        self._init_netcdf()
        LOG.info("band: %d, bit_depth: %d, bit_mask: %d, fill: %d" %
                 (self.band, self.bit_depth, self.bit_mask, self.fill))

    def _init_netcdf(self):
        self.nc.set_fill_on()
        self.nc.createDimension('y', self.size[0])
        chunksize = self._get_chunksize()
        self.nc.createVariable('y', 'i2', ('y',), zlib=True, complevel=CSPP_GEO_GRBR_IMAGE_COMPRESSION)
        self.nc.variables["y"][:] = range(self.size[0])
        self.nc.createDimension('x', self.size[1])
        self.nc.createVariable('x', 'i2', ('x',), zlib=True, complevel=CSPP_GEO_GRBR_IMAGE_COMPRESSION)
        self.nc.variables["x"][:] = range(self.size[1])
        self.ncrad = self.nc.createVariable(
            'Rad', 'i2', ('y', 'x'), fill_value=self.fill, zlib=True, complevel=CSPP_GEO_GRBR_IMAGE_COMPRESSION, chunksizes=chunksize)
        self.ncrad.set_auto_maskandscale(False)
        self.ncdqf = self.nc.createVariable(
            'DQF', 'i1', ('y', 'x'), fill_value=255, zlib=True, complevel=CSPP_GEO_GRBR_IMAGE_COMPRESSION, chunksizes=chunksize)
        self.ncdqf.set_auto_maskandscale(False)
        self.nc.sync()

    def track(self, ul_x, ul_y, br_x, br_y):
        if CSPP_GEO_GRBR_ENABLE_TRACKING:
            self.tracking_file.write("%d %d %d %d\n" % (ul_x, ul_y, br_x, br_y))

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

        rad = rad & self.bit_mask  # apply bit depth

        ul_x, ul_y, br_x, br_y = self._ulbr(hp, rad.shape)
        self.ncrad[ul_y:br_y, ul_x:br_x] = rad
        self.ncdqf[ul_y:br_y, ul_x:br_x] = dqf

        self.track(ul_x, ul_y, br_x, br_y)
        self.nc.sync()

        self.pixels_seen += (rad.shape[0] * rad.shape[1])
        LOG.debug("Done adding data...")

    def _ulbr(self, hp, shape):
        h, w = shape
        ul_x, ul_y = (hp.ul_x, hp.ul_y)
        # FIXME: handling for 24-bit, see struct
        row_offset = (hp.row_offset << 8) + hp.row_offsetB
        ul_y = ul_y + row_offset
        br_x = ul_x + w
        br_y = ul_y + h
        return ul_x, ul_y, br_x, br_y

    def _get_chunksize(self):
        b = band(self.apid)
        ABI_Band = ABI_Bands[b].chunk_size
        return ABI_Band

    def _get_size(self):
        b = band(self.apid)
        ABI_Band = ABI_Bands[b]
        abi_type = apid2region(self.apid)
        return ABI_Resolutions[abi_type][ABI_Band.km]

    def _get_depth(self):
        b = band(self.apid)
        ABI_Band = ABI_Bands[b]
        return ABI_Band.bit_depth
