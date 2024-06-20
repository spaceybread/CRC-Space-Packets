#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tools for reconstructing MAG

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

import ctypes
import numpy as np

from grbr.dataset import GRBStruct, GRBDataset

import logging
LOG = logging.getLogger('GRB-R')

# 7.6.1 - Geomagnetic Field Product


class MAG_DATA_STRUCT(GRBStruct):
    _pack_ = 1
    _fields_ = [("_cf_IB_data", ctypes.c_uint64 * 2),
                ("IB_data", ctypes.c_float * 3 * 10),
                ("_cf_OB_data", ctypes.c_uint64 * 2),
                ("OB_data", ctypes.c_float * 3 * 10),
                ("_cf_IB_mag_ACRF", ctypes.c_uint64 * 2),
                ("IB_mag_ACRF", ctypes.c_float * 3 * 10),
                ("_cf_OB_mag_ACRF", ctypes.c_uint64 * 2),
                ("OB_mag_ACRF", ctypes.c_float * 3 * 10),
                ("_cf_IB_mag_ECI", ctypes.c_uint64 * 2),
                ("IB_mag_ECI", ctypes.c_float * 3 * 10),
                ("_cf_OB_mag_ECI", ctypes.c_uint64 * 2),
                ("OB_mag_ECI", ctypes.c_float * 3 * 10),
                ("_cf_IB_mag_EPN", ctypes.c_uint64 * 2),
                ("IB_mag_EPN", ctypes.c_float * 3 * 10),
                ("_cf_OB_mag_EPN", ctypes.c_uint64 * 2),
                ("OB_mag_EPN", ctypes.c_float * 3 * 10),
                ("_cf_IB_mag_BRF", ctypes.c_uint64 * 2),
                ("IB_mag_BRF", ctypes.c_float * 3 * 10),
                ("_cf_OB_mag_BRF", ctypes.c_uint64 * 2),
                ("OB_mag_BRF", ctypes.c_float * 3 * 10),
                ("_cf_amb_mag_EPN", ctypes.c_uint64 * 2),
                ("amb_mag_EPN", ctypes.c_float * 3 * 10),
                ("_cf_amb_mag_ECI", ctypes.c_uint64 * 2),
                ("amb_mag_ECI", ctypes.c_float * 3 * 10),
                ("_cf_amb_mag_BRF", ctypes.c_uint64 * 2),
                ("amb_mag_BRF", ctypes.c_float * 3 * 10),
                ("_cf_total_mag_ACRF", ctypes.c_uint64),
                ("total_mag_ACRF", ctypes.c_float * 10),
                ("_cf_DQF", ctypes.c_uint64),
                ("DQF", ctypes.c_uint32 * 10),
                ("_cf_IB_status", ctypes.c_uint64),
                ("IB_status", ctypes.c_uint16 * 10),
                ("_cf_OB_status", ctypes.c_uint64),
                ("OB_status", ctypes.c_uint16 * 10),
                ("Instrument_ID", ctypes.c_uint8 * 2),
                ("yaw_flip", ctypes.c_uint8),
                ("eclipse_flag", ctypes.c_uint8),
                ("_cf_IB_time", ctypes.c_uint64),
                ("IB_time", ctypes.c_double * 10),
                ("_cf_OB_time", ctypes.c_uint64),
                ("OB_time", ctypes.c_double * 10),
                ("attitude_quat_Q0", ctypes.c_double),
                ("attitude_quat_Q1", ctypes.c_double),
                ("attitude_quat_Q2", ctypes.c_double),
                ("attitude_quat_Q3", ctypes.c_double),
                ("ECEF_X", ctypes.c_float),
                ("ECEF_Y", ctypes.c_float),
                ("ECEF_Z", ctypes.c_float),
                ("orbit_quat_Q0", ctypes.c_double),
                ("orbit_quat_Q1", ctypes.c_double),
                ("orbit_quat_Q2", ctypes.c_double),
                ("orbit_quat_Q3", ctypes.c_double),
                ("quat_timestamp", ctypes.c_double),
                ("_cf_solar_array_current", ctypes.c_uint64),
                ("solar_array_current", ctypes.c_uint16 * 4),
                ]

class MAG_DATA_STRUCT_DO0801(GRBStruct):
    _pack_ = 1
    _fields_ = [("_cf_IB_data_uncorrected", ctypes.c_uint64 * 2),
                ("IB_data_uncorrected", ctypes.c_float * 3 * 10),
                ("_cf_OB_data_uncorrected", ctypes.c_uint64 * 2),
                ("OB_data_uncorrected", ctypes.c_float * 3 * 10),
                ("_cf_IB_mag_ACRF_uncorrected", ctypes.c_uint64 * 2),
                ("IB_mag_ACRF_uncorrected", ctypes.c_float * 3 * 10),
                ("_cf_OB_mag_ACRF_uncorrected", ctypes.c_uint64 * 2),
                ("OB_mag_ACRF_uncorrected", ctypes.c_float * 3 * 10),

                ("_cf_IB_mag_BRF_uncorrected", ctypes.c_uint64 * 2),
                ("IB_mag_BRF_uncorrected", ctypes.c_float * 3 * 10),
                ("_cf_OB_mag_BRF_uncorrected", ctypes.c_uint64 * 2),
                ("OB_mag_BRF_uncorrected", ctypes.c_float * 3 * 10),
                ("_cf_IB_mag_ECI_uncorrected", ctypes.c_uint64 * 2),
                ("IB_mag_ECI_uncorrected", ctypes.c_float * 3 * 10),
                ("_cf_OB_mag_ECI_uncorrected", ctypes.c_uint64 * 2),
                ("OB_mag_ECI_uncorrected", ctypes.c_float * 3 * 10),
                ("_cf_IB_mag_EPN_uncorrected", ctypes.c_uint64 * 2),
                ("IB_mag_EPN_uncorrected", ctypes.c_float * 3 * 10),
                ("_cf_OB_mag_EPN_uncorrected", ctypes.c_uint64 * 2),
                ("OB_mag_EPN_uncorrected", ctypes.c_float * 3 * 10),

                ("_cf_total_mag_ACRF_uncorrected", ctypes.c_uint64),
                ("total_mag_ACRF_uncorrected", ctypes.c_float * 10),
                ("_cf_amb_mag_BRF_uncorrected", ctypes.c_uint64 * 2),
                ("amb_mag_BRF_uncorrected", ctypes.c_float * 3 * 10),
                ("_cf_amb_mag_ECI_uncorrected", ctypes.c_uint64 * 2),
                ("amb_mag_ECI_uncorrected", ctypes.c_float * 3 * 10),
                ("_cf_amb_mag_EPN_uncorrected", ctypes.c_uint64 * 2),
                ("amb_mag_EPN_uncorrected", ctypes.c_float * 3 * 10),
                ("_cf_IB_data", ctypes.c_uint64 * 2),
                ("IB_data", ctypes.c_float * 3 * 10),
                ("_cf_OB_data", ctypes.c_uint64 * 2),
                ("OB_data", ctypes.c_float * 3 * 10),
                ("_cf_IB_mag_ACRF", ctypes.c_uint64 * 2),
                ("IB_mag_ACRF", ctypes.c_float * 3 * 10),

                ("_cf_OB_mag_ACRF", ctypes.c_uint64 * 2),
                ("OB_mag_ACRF", ctypes.c_float * 3 * 10),
                ("_cf_IB_mag_BRF", ctypes.c_uint64 * 2),
                ("IB_mag_BRF", ctypes.c_float * 3 * 10),
                ("_cf_OB_mag_BRF", ctypes.c_uint64 * 2),
                ("OB_mag_BRF", ctypes.c_float * 3 * 10),
                ("_cf_IB_mag_ECI", ctypes.c_uint64 * 2),
                ("IB_mag_ECI", ctypes.c_float * 3 * 10),
                ("_cf_OB_mag_ECI", ctypes.c_uint64 * 2),
                ("OB_mag_ECI", ctypes.c_float * 3 * 10),

                ("_cf_IB_mag_EPN", ctypes.c_uint64 * 2),
                ("IB_mag_EPN", ctypes.c_float * 3 * 10),
                ("_cf_OB_mag_EPN", ctypes.c_uint64 * 2),
                ("OB_mag_EPN", ctypes.c_float * 3 * 10),
                ("_cf_total_mag_ACRF", ctypes.c_uint64),
                ("total_mag_ACRF", ctypes.c_float * 10),
                ("_cf_amb_mag_BRF", ctypes.c_uint64 * 2),
                ("amb_mag_BRF", ctypes.c_float * 3 * 10),
                ("_cf_amb_mag_ECI", ctypes.c_uint64 * 2),
                ("amb_mag_ECI", ctypes.c_float * 3 * 10),

                ("_cf_amb_mag_EPN", ctypes.c_uint64 * 2),
                ("amb_mag_EPN", ctypes.c_float * 3 * 10),
                ("_cf_DQF", ctypes.c_uint64),
                ("DQF", ctypes.c_uint32 * 10),
                ("_cf_IB_status", ctypes.c_uint64),
                ("IB_status", ctypes.c_uint16 * 10),
                ("_cf_OB_status", ctypes.c_uint64),
                ("OB_status", ctypes.c_uint16 * 10),
                ("Instrument_ID", ctypes.c_uint8 * 2),
                ("yaw_flip", ctypes.c_uint8),

                ("eclipse_flag", ctypes.c_uint8),
                ("_cf_IB_time", ctypes.c_uint64),
                ("IB_time", ctypes.c_double * 10),
                ("_cf_OB_time", ctypes.c_uint64),
                ("OB_time", ctypes.c_double * 10),
                ("attitude_quat_Q0", ctypes.c_double),
                ("attitude_quat_Q1", ctypes.c_double),
                ("attitude_quat_Q2", ctypes.c_double),
                ("attitude_quat_Q3", ctypes.c_double),
                ("ECEF_X", ctypes.c_float),
                ("ECEF_Y", ctypes.c_float),
                ("ECEF_Z", ctypes.c_float),
                ("orbit_quat_Q0", ctypes.c_double),
                ("orbit_quat_Q1", ctypes.c_double),
                ("orbit_quat_Q2", ctypes.c_double),
                ("orbit_quat_Q3", ctypes.c_double),

                ("quat_timestamp", ctypes.c_double),
                ("_cf_solar_array_current", ctypes.c_uint64),
                ("solar_array_current", ctypes.c_uint16 * 4),
                ]

BAD_FIELDS = [
]

# print "DEBUG: sizeof MAG_DATA_STRUCT_DO0801:", ctypes.sizeof(MAG_DATA_STRUCT_DO0801)
# start=0
# for field in MAG_DATA_STRUCT_DO0801._fields_:
#     print "DEBUG: byte", start, "sizeof", field[0], ":", ctypes.sizeof(field[1])
#     start=start+ctypes.sizeof(field[1])
# 
# print "DEBUG: sizeof MAG_DATA_STRUCT:", ctypes.sizeof(MAG_DATA_STRUCT)
# start=0
# for field in MAG_DATA_STRUCT._fields_:
#     print "DEBUG: byte", start, "sizeof", field[0], ":", ctypes.sizeof(field[1])
#     start=start+ctypes.sizeof(field[1])

class MAG(GRBDataset):
    track = False

    def __init__(self, h1, h2, hp):
        super(MAG, self).__init__(h1, h2, hp)
        self.fields = {}
        self.count = 0

    def _add_metadata(self, h1, h2, hp, p):
        super(MAG, self)._add_metadata(h1, h2, hp, p)
        self._sync_to_nc()


    def _add_data(self, h1, h2, hp, p):
        p = self._decompress(hp, p)
        LOG.info("Adding data payload of size: %d" % len(p))
        if len(p) == ctypes.sizeof(MAG_DATA_STRUCT):
            data_struct = MAG_DATA_STRUCT()
        elif len(p) == ctypes.sizeof(MAG_DATA_STRUCT_DO0801):
            data_struct = MAG_DATA_STRUCT_DO0801()
        else:
            raise(RuntimeError, "MAG GEOF payload of size %d bytes does not match any known configurations" % (len(p)))
        data_struct.receiveSome(p)

        for field_name, field_type in data_struct._fields_:
            if field_name.startswith("_cf_"):
                LOG.debug("skipping control field %s" % (field_name))
                continue

            field_data = getattr(data_struct, field_name)
            try:
                field_data = np.ctypeslib.as_array(field_data)
            except AttributeError:
                pass  # TODO: if it's already a long, etc, it won't be able to be made an array

            # adds a dimension for report #
            field_data = np.expand_dims(field_data, 0)
            if field_name in self.fields:
                self.fields[field_name] = np.vstack(
                    (self.fields[field_name], field_data))
            else:
                self.fields[field_name] = field_data

        self.count = self.count + 1

        if self.ncml:
            self._sync_to_nc()


    def _sync_to_nc(self):
        for field_name in self.fields.keys():
            LOG.info("Adding %s" % field_name)
#      LOG.debug("SHAPE %s must match %s" % (self.nc.variables[field_name].shape, self.fields[field_name].shape))
#      LOG.debug(self.fields[field_name][:])
            try:
                self.nc.variables[field_name][:] = self.fields[field_name][:]
            except Exception as e:
                LOG.error("Unexpected error: %s" % e)
        self.nc.sync()
