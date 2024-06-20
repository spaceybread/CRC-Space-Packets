#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tools for reconstructing GLM strikes

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

# 7.2.1.6.1

class GLM_FLASH_STRUCT(GRBStruct):
    _pack_ = 1
    _fields_ = [("flash_id", ctypes.c_uint16),
                ("flash_time_offset_of_first_event", ctypes.c_int16),
                ("flash_time_offset_of_last_event", ctypes.c_int16),
                ("flash_lat", ctypes.c_float),
                ("flash_lon", ctypes.c_float),
                ("flash_area", ctypes.c_uint16),
                ("flash_energy", ctypes.c_uint16),
                ("flash_quality_flag", ctypes.c_uint16),
                ]


class GLM_FLASH_STRUCT_DO07(GRBStruct):
    _pack_ = 1
    _fields_ = [("flash_id", ctypes.c_uint16),
                ("flash_time_offset_of_first_event", ctypes.c_int16),
                ("flash_time_offset_of_last_event", ctypes.c_int16),
                ("flash_frame_time_offset_of_first_event", ctypes.c_int16),
                ("flash_frame_time_offset_of_last_event", ctypes.c_int16),
                ("flash_lat", ctypes.c_float),
                ("flash_lon", ctypes.c_float),
                ("flash_area", ctypes.c_uint16),
                ("flash_energy", ctypes.c_uint16),
                ("flash_quality_flag", ctypes.c_uint16),
                ]


class GLM_GROUP_STRUCT(GRBStruct):
    _pack_ = 1
    _fields_ = [("group_id", ctypes.c_uint32),
                ("group_time_offset", ctypes.c_int16),
#                ("group_frame_time_offset", ctypes.c_int16),
                ("group_lat", ctypes.c_float),
                ("group_lon", ctypes.c_float),
                ("group_area", ctypes.c_uint16),
                ("group_energy", ctypes.c_uint16),
                ("group_parent_flash_id", ctypes.c_uint16),
                ("group_quality_flag", ctypes.c_uint16),
                ]

class GLM_GROUP_STRUCT_DO07(GRBStruct):
    _pack_ = 1
    _fields_ = [("group_id", ctypes.c_uint32),
                ("group_time_offset", ctypes.c_int16),
                ("group_frame_time_offset", ctypes.c_int16),
                ("group_lat", ctypes.c_float),
                ("group_lon", ctypes.c_float),
                ("group_area", ctypes.c_uint16),
                ("group_energy", ctypes.c_uint16),
                ("group_parent_flash_id", ctypes.c_uint16),
                ("group_quality_flag", ctypes.c_uint16),
                ]

class GLM_EVENT_STRUCT(GRBStruct):
    _pack_ = 1
    _fields_ = [("event_id", ctypes.c_uint32),
                ("event_time_offset", ctypes.c_int16),
                ("event_lat", ctypes.c_uint16),
                ("event_lon", ctypes.c_uint16),
                ("event_energy", ctypes.c_uint16),
                ("event_parent_group_id", ctypes.c_uint32),
                ]

#print "DEBUG: sizeof GLM_FLASH_STRUCT:", ctypes.sizeof(GLM_FLASH_STRUCT)
#print "DEBUG: sizeof GLM_GROUP_STRUCT:", ctypes.sizeof(GLM_GROUP_STRUCT)
#print "DEBUG: sizeof GLM_EVENT_STRUCT:", ctypes.sizeof(GLM_EVENT_STRUCT)


class GLM(GRBDataset):
    track = False

    def __init__(self, h1, h2, hp):
        super(GLM, self).__init__(h1, h2, hp)
        self.fields = {}
        self.fcount = self.gcount = self.ecount = 0

    def _add_metadata(self, h1, h2, hp, p):
        super(GLM, self)._add_metadata(h1, h2, hp, p)
        self._sync_to_nc()

    def _add_data(self, h1, h2, hp, p):
        LOG.info("Adding data payload...")
        p = self._decompress(hp, p)

        if h1.apid == 0x301:
            self._add_event(h1, h2, hp, p)
        elif h1.apid == 0x302:
            self._add_flash(h1, h2, hp, p)
        elif h1.apid == 0x303:
            self._add_group(h1, h2, hp, p)
        else:
            raise(NotImplementedError, "APID %s is not GLM?" % (h1.apid))

    def _add_flash(self, h1, h2, hp, p):
        LOG.debug("Adding flash...")
        nFlashes = ctypes.c_uint64.from_buffer_copy(p[:8]).value
        if len(p)-8 == nFlashes * ctypes.sizeof(GLM_FLASH_STRUCT): # FIXME: the minus 8 is due to ignoring the first field in the GLM struct; this should be added and ignored elsewhere
            LOG.info("Using GLM_FLASH_STRUCT")
            self._parse_glm(GLM_FLASH_STRUCT, p)
        elif len(p)-8 == nFlashes * ctypes.sizeof(GLM_FLASH_STRUCT_DO07):
            LOG.info("Using GLM_FLASH_STRUCT_DO07")
            self._parse_glm(GLM_FLASH_STRUCT_DO07, p)
        else:
            LOG.error("sizeof GLM_FLASH_STRUCT: %d", ctypes.sizeof(GLM_FLASH_STRUCT))
            LOG.error("sizeof GLM_FLASH_STRUCT_DO07: %d", ctypes.sizeof(GLM_FLASH_STRUCT_DO07))
            raise(RuntimeError, "unrecognized GLM flash payload size: %d" % (len(p)))
        self.fcount = self.fcount + 1

    def _add_group(self, h1, h2, hp, p):
        LOG.debug("Adding group...")
        nGroups = ctypes.c_uint64.from_buffer_copy(p[:8]).value
        if len(p)-8 == nGroups * ctypes.sizeof(GLM_GROUP_STRUCT): # FIXME: the minus 8 is due to ignoring the first field in the GLM struct; this should be added and ignored elsewhere
            LOG.info("Using GLM_GROUP_STRUCT")
            self._parse_glm(GLM_GROUP_STRUCT, p)
        elif len(p)-8 == nGroups * ctypes.sizeof(GLM_GROUP_STRUCT_DO07):
            LOG.info("Using GLM_GROUP_STRUCT_DO07")
            self._parse_glm(GLM_GROUP_STRUCT_DO07, p)
        else:
            LOG.error("sizeof GLM_GROUP_STRUCT: %d", ctypes.sizeof(GLM_GROUP_STRUCT))
            LOG.error("sizeof GLM_GROUP_STRUCT_DO07: %d", ctypes.sizeof(GLM_GROUP_STRUCT_DO07))
            raise(RuntimeError, "unrecognized GLM flash payload size: %d" % (len(p)))
        self.gcount = self.gcount + 1

    def _add_event(self, h1, h2, hp, p):
        LOG.debug("Adding event...")
        self._parse_glm(GLM_EVENT_STRUCT, p)
        self.ecount = self.ecount + 1


    def _parse_glm(self, glm_struct, p):
        count = ctypes.c_uint64.from_buffer_copy(p[:8]).value
        LOG.info("GLM data points in payload: %s" % (count))
        if count < 1: # if there's no data, bail
            if len(p) > 8: # if there's no data but the payload contains something, there's probably a problem
                LOG.warn("GLM payload has a non-zero size but claimed no data...")
            return

        glm_structs = []
        size = ctypes.sizeof(glm_struct)
        for i in range(count):
            offset = 8 + (i * size)
            new = glm_struct()
            new.receiveSome(p[offset:offset + size])
            glm_structs.append(new)

        for field_name, field_type in glm_structs[0]._fields_:
            field_data = [getattr(s, field_name) for s in glm_structs]
#      field_data = (field_type * len(field_data))(*field_data) # convert to ctypes array of correct type
#      LOG.debug("%s %s %s" % (field_name, field_type, field_data))
            # FIXME: will dtype be a problem here?
            if field_name in self.fields:
                self.fields[field_name] = np.concatenate(
                    (self.fields[field_name], field_data))
            else:
                self.fields[field_name] = np.array(
                    field_data, dtype=field_type)
#        LOG.debug("copied to fields: %s %s" % (self.fields[field_name].dtype, self.fields[field_name]))
        if self.ncml:
            self._sync_to_nc()

    def _sync_to_nc(self):
        for field_name in self.fields.keys():
            #      LOG.debug("syncing %s %s %s" % (field_name, self.fields[field_name][:].dtype, self.fields[field_name][:]))
            v = self.nc.variables[field_name]
            v.set_auto_maskandscale(False)
            v[:] = self.fields[field_name][:]
            LOG.debug("synced %s %s %s" % (field_name, v.dtype, v[:]))
        self.nc.sync()
