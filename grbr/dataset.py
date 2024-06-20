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

import os
import string
import ctypes
from datetime import datetime

from netCDF4 import Dataset

import grbr.szip
import grbr.jpeg2k
import grbr.apid
from grbr.ncml import update_nc_from_ncml
from grbr.cache import product_tmpname, datetime_from_hp
from grbr.config import CSPP_GEO_GRBR_TMP, CSPP_GEO_GRBR_OUT, CSPP_GEO_GRBR_TRACK, CSPP_GEO_GRBR_ENABLE_TRACKING, VERSION, CSPP_GEO_GRBR_DEBUG
from grbr.config import CSPP_GEO_GRB_POST_PROCESS_SCRIPT
from grbr.eventlog import log_start, log_end, log_error, log_timeout
from grbr.utils import generate_history_string

import subprocess
import socket
import logging
LOG = logging.getLogger('GRB-R')


class GRBStruct(ctypes.LittleEndianStructure):

    def receiveSome(self, bytes):
        fit = min(len(bytes), ctypes.sizeof(self))
        ctypes.memmove(ctypes.addressof(self), bytes, fit)


def _dump_struct(astruct):
    for field_name, field_type in astruct._fields_:
        LOG.debug("%s: %s" % (field_name, getattr(astruct, field_name)))


class GRBDataset(object):
    track = False

    def __init__(self, h1, h2, hp):
        self.fstub = os.path.join(
            CSPP_GEO_GRBR_TMP, product_tmpname(h1, h2, hp))
        self.product_time = datetime_from_hp(hp)
        self.product_name = grbr.apid.apids[h1.apid]
        self.ncname = self.fstub + ".nc"
        self.ncmlname = self.fstub + ".ncml"
        log_start(self.product_name, self.product_time, self.ncname)
        if os.path.exists(self.ncname):
            mode = 'r+'
        else:
            mode = 'w'
        self.nc = Dataset(self.ncname, mode, format='NETCDF4')
#        setattr(self.nc, "cspp_geo_grb_reconstruction_start_time", str(datetime.utcnow()))
        if CSPP_GEO_GRBR_ENABLE_TRACKING and self.track:
            self.tracking_file = open(os.path.join(CSPP_GEO_GRBR_TRACK, product_tmpname(h1, h2, hp) + ".track"), 'a', buffering=1)  # line buffered
        self.ncml = None
        self.metadata_complete = False

    def add_bundle(self, h1, h2, hp, p):
        if grbr.apid.isMetadata(h1.apid):
            self._add_metadata(h1, h2, hp, p)
        elif grbr.apid.isData(h1.apid):
            self._add_data(h1, h2, hp, p)
        else:
            raise(NotImplementedError, "APID %s is not recognized!" % (hex(h1.apid)))

        if self.finished():
            self.finalize()

    def cleanup(self):
        for ext in [".pipe", ".track", ".ncml"]:
            if not CSPP_GEO_GRBR_DEBUG:
                extra = self.fstub + ext
                try:
                    os.unlink(extra)
                except:
                    continue

    def finished(self):
        # For now, we assume the metadata always comes last and once we've added
        # the metadata, we're finished.
        return self.metadata_complete

    def track(self):
        pass

    def finalize(self):
        if CSPP_GEO_GRBR_ENABLE_TRACKING and self.track:
            self.tracking_file.close()
        LOG.info("Finalizing product...")
        try:
            finalname = os.path.join(CSPP_GEO_GRBR_OUT, self.nc.dataset_name)
        except:
            log_error(self.product_name, self.product_time, self.ncname)
            LOG.error("Final dataset name could not be determined. The metadata (ncml) may be invalid.")
            exit(1)
        setattr(self.nc, "cspp_geo_grb_reconstruction_end_time", str(datetime.utcnow()))
        self.nc.close()
        tmpname = self.fstub + ".nc"
        LOG.info("Moving %s to %s" % (tmpname, finalname))
        os.rename(tmpname, finalname)
        LOG.info("Complete!")
        log_end(self.product_name, self.product_time, finalname)
        if CSPP_GEO_GRB_POST_PROCESS_SCRIPT != "":
            LOG.info("Executing post process script:")
            cmd = [CSPP_GEO_GRB_POST_PROCESS_SCRIPT, finalname]
            LOG.info(" ".join(cmd))
            subprocess.Popen(cmd, start_new_session=True)
        self.cleanup()
        exit(0)

    def handle_timeout(self):
        log_timeout(self.product_name, self.product_time, self.ncname)

    def _add_metadata(self, h1, h2, hp, p):
        LOG.info("Adding metadata payload...")
        ncml = str(self._decompress(hp, p))

        # FIXME: tweak to cut garbage from the end of szip'd metadata
        end = str.find(ncml, '</netcdf>') + len('</netcdf>')
        ncml = ncml[:end]

        if self.ncml:
            LOG.warning(
                "Received a second set of metadata for the same dataset.")
            if self.ncml == ncml:
                LOG.warning("Fortunately they match, continuing...")
            else:
                LOG.error(
                    "Received a second set of metadata that DOES NOT match the previous; output may be invalid! (Likely caused by an invalid timestamp field.)")
            return
        else:
            self.ncml = ncml

        # FIXME: any reason we don't want to always write ncml to disk? i like
        # it now...
        f = open(self.ncmlname, 'w')
        f.write(ncml)
        f.close()

        self.nc = update_nc_from_ncml(self.nc, self.ncmlname, format='NETCDF4')
        setattr(self.nc, "cspp_geo_grb_version", "CSPP Geo GRB v%s" % (VERSION))
        setattr(self.nc, "cspp_geo_grb_production_host", socket.gethostname())
        setattr(self.nc, "history", generate_history_string())
        LOG.info("Done adding metadata...")
        self.metadata_complete = True

    def _add_data(self, h1, h2, hp, p):
        raise(NotImplementedError)  # stub

    def _decompress(self, hp, p):
        if hp.compression_algorithm == 0:
            return p
        elif hp.compression_algorithm == 1:
            # FIXME: this probably won't actually work, getting back a 2d
            # array, can GLM even be j2k?
            return grbr.jpeg2k.decompress(p)
        elif hp.compression_algorithm == 2:
            return grbr.szip.decompress(p)
        else:
            raise(NotImplementedError)
