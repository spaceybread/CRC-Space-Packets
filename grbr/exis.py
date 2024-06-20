#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tools for reconstructing EXIS

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

from grbr.dataset import GRBStruct, GRBDataset

import sys

import ctypes
import numpy as np

import logging
LOG = logging.getLogger('GRB-R')


# Table 7.4.1.5.1 Solar Flux: EUV Product Data

class EXIS_EUV_STRUCT(GRBStruct):
    _pack_ = 1
    _fields_ = [("_cf_irradianceSpectrum", ctypes.c_uint64),
                ("irradianceSpectrum", ctypes.c_float * 23),
                ("time",    ctypes.c_double),
                ("_cf_lowWavelength",  ctypes.c_uint64),
                ("lowWavelength",   ctypes.c_float * 23),
                ("_cf_highWavelength", ctypes.c_uint64),
                ("highWavelength",  ctypes.c_float * 23),
                ("EUV_CaseNumber",  ctypes.c_uint8),
                ("qualityFlags",    ctypes.c_uint64),
                ("quaternion_Q0",   ctypes.c_float),
                ("quaternion_Q1",   ctypes.c_float),
                ("quaternion_Q2",   ctypes.c_float),
                ("quaternion_Q3",   ctypes.c_float),
                ("ECEF_X", ctypes.c_float),
                ("ECEF_Y", ctypes.c_float),
                ("ECEF_Z", ctypes.c_float),
                ("au_factor",   ctypes.c_float),
                ("SC_yaw_flip_flag",    ctypes.c_uint8),
                ("nXRS",    ctypes.c_uint8),
                ("nGoodXRSA",   ctypes.c_uint8),
                ("nGoodXRSB",   ctypes.c_uint8),
                ("nEUVSA",  ctypes.c_uint8),
                ("nGood256",    ctypes.c_uint8),
                ("nGood284",    ctypes.c_uint8),
                ("nGood304",    ctypes.c_uint8),
                ("nEUVSB",  ctypes.c_uint8),
                ("nGood1175",   ctypes.c_uint8),
                ("nGood1216",   ctypes.c_uint8),
                ("nGood1335",   ctypes.c_uint8),
                ("nGood1405",   ctypes.c_uint8),
                ("nEUVSC",  ctypes.c_uint8),
                ("nGoodMg", ctypes.c_uint8),
                ("_cf_xrsQualityFlags",    ctypes.c_uint64),
                ("xrsQualityFlags", ctypes.c_uint32 * 30),
                ("_cf_euvsaQualityFlags",  ctypes.c_uint64),
                ("euvsaQualityFlags",   ctypes.c_uint32 * 30),
                ("_cf_euvsbQualityFlags",  ctypes.c_uint64),
                ("euvsbQualityFlags",   ctypes.c_uint32 * 30),
#                ("_cf_euvscQualityFlags",  ctypes.c_uint64),
#                ("euvscQualityFlags",   ctypes.c_uint32 * 15),
                ("euvsaAvgTemp",    ctypes.c_float),
                ("euvsbAvgTemp",    ctypes.c_float),
                ("euvsc1AvgTemp",   ctypes.c_float),
                ("euvsc2AvgTemp",   ctypes.c_float),
                ("avgIrradianceXRSA",   ctypes.c_float),
                ("avgIrradianceXRSB",   ctypes.c_float),
                ("avgIrradiance256",    ctypes.c_float),
                ("avgIrradiance284",    ctypes.c_float),
                ("avgIrradiance304",    ctypes.c_float),
                ("avgIrradiance1175",   ctypes.c_float),
                ("avgIrradiance1216",   ctypes.c_float),
                ("avgIrradiance1335",   ctypes.c_float),
                ("avgIrradiance1405",   ctypes.c_float),
                ("avgRatioMgExis",  ctypes.c_float),
                ("avgRatioMgNoaa",  ctypes.c_float),
                ("dailyIrradiance256",  ctypes.c_float),
                ("dailyIrradiance284",  ctypes.c_float),
                ("dailyIrradiance304",  ctypes.c_float),
                ("dailyIrradiance1175", ctypes.c_float),
                ("dailyIrradiance1216", ctypes.c_float),
                ("dailyIrradiance1335", ctypes.c_float),
                ("dailyIrradiance1405", ctypes.c_float),
                ("dailyRatioMgNoaa",    ctypes.c_float),
                ("Average_SPS_dispersion_angle",    ctypes.c_float),
                ("Average_SPS_cross_dispersion_angle",  ctypes.c_float),
                ("_cf_solar_array_current",    ctypes.c_uint64),
                ("solar_array_current", ctypes.c_uint16 * 4),
                ("SC_eclipse_flag", ctypes.c_uint8),
                ("euvscIntegrationTime", ctypes.c_float),
                ("_cf_euvscQualityFlags", ctypes.c_uint64),
                ("euvscQualityFlags", ctypes.c_uint32 * 10),
                ("Total_SPS_angles", ctypes.c_uint8),
                ("Total_valid_SPS_angle_pairs", ctypes.c_uint8),
                ("euvscActiveChannel", ctypes.c_uint8),
                ]


class EXIS_EUV_STRUCT_DO07(GRBStruct):
    _pack_ = 1
    _fields_ = [("_cf_irradianceSpectrum", ctypes.c_uint64),
                ("irradianceSpectrum", ctypes.c_float * 23),
                ("time",    ctypes.c_double),
                ("_cf_lowWavelength",  ctypes.c_uint64),
                ("lowWavelength",   ctypes.c_float * 23),
                ("_cf_highWavelength", ctypes.c_uint64),
                ("highWavelength",  ctypes.c_float * 23),
                ("EUV_CaseNumber",  ctypes.c_uint8),
                ("qualityFlags",    ctypes.c_uint64),
                ("quaternion_Q0",   ctypes.c_float),
                ("quaternion_Q1",   ctypes.c_float),
                ("quaternion_Q2",   ctypes.c_float),
                ("quaternion_Q3",   ctypes.c_float),
                ("ECEF_X", ctypes.c_float),
                ("ECEF_Y", ctypes.c_float),
                ("ECEF_Z", ctypes.c_float),
                ("au_factor",   ctypes.c_float),
                ("SC_yaw_flip_flag",    ctypes.c_uint8),
                ("nXRS",    ctypes.c_uint8),
                ("nGoodXRSA",   ctypes.c_uint8),
                ("nGoodXRSB",   ctypes.c_uint8),
                ("nEUVSA",  ctypes.c_uint8),
                ("nGood256",    ctypes.c_uint8),
                ("nGood284",    ctypes.c_uint8),
                ("nGood304",    ctypes.c_uint8),
                ("nEUVSB",  ctypes.c_uint8),
                ("nGood1175",   ctypes.c_uint8),
                ("nGood1216",   ctypes.c_uint8),
                ("nGood1335",   ctypes.c_uint8),
                ("nGood1405",   ctypes.c_uint8),
                ("nEUVSC",  ctypes.c_uint8),
                ("nGoodMg", ctypes.c_uint8),
                ("_cf_xrsQualityFlags",    ctypes.c_uint64),
                ("xrsQualityFlags", ctypes.c_uint32 * 30),
                ("_cf_euvsaQualityFlags",  ctypes.c_uint64),
                ("euvsaQualityFlags",   ctypes.c_uint32 * 30),
                ("_cf_euvsbQualityFlags",  ctypes.c_uint64),
                ("euvsbQualityFlags",   ctypes.c_uint32 * 30),
#                ("_cf_euvscQualityFlags",  ctypes.c_uint64),
#                ("euvscQualityFlags",   ctypes.c_uint32 * 15),
                ("euvsaAvgTemp",    ctypes.c_float),
                ("euvsbAvgTemp",    ctypes.c_float),
                ("euvsc1AvgTemp",   ctypes.c_float),
                ("euvsc2AvgTemp",   ctypes.c_float),
                ("avgIrradianceXRSA",   ctypes.c_float),
                ("avgIrradianceXRSB",   ctypes.c_float),
                ("avgIrradiance256",    ctypes.c_float),
                ("avgIrradiance284",    ctypes.c_float),
                ("avgIrradiance304",    ctypes.c_float),
                ("avgIrradiance1175",   ctypes.c_float),
                ("avgIrradiance1216",   ctypes.c_float),
                ("avgIrradiance1335",   ctypes.c_float),
                ("avgIrradiance1405",   ctypes.c_float),
                ("avgRatioMgExis",  ctypes.c_float),
                ("avgRatioMgNoaa",  ctypes.c_float),
                ("dailyIrradiance256",  ctypes.c_float),
                ("dailyIrradiance284",  ctypes.c_float),
                ("dailyIrradiance304",  ctypes.c_float),
                ("dailyIrradiance1175", ctypes.c_float),
                ("dailyIrradiance1216", ctypes.c_float),
                ("dailyIrradiance1335", ctypes.c_float),
                ("dailyIrradiance1405", ctypes.c_float),
                ("dailyRatioMgNoaa",    ctypes.c_float),
                ("_cf_ObservationTimesEUVSA",  ctypes.c_uint64),
                ("ObservationTimesEUVSA", ctypes.c_double * 30),
                ("_cf_ObservationTimesEUVSB",  ctypes.c_uint64),
                ("ObservationTimesEUVSB", ctypes.c_double * 30),
                ("_cf_ObservationTimesEUVSC",  ctypes.c_uint64),
                ("ObservationTimesEUVSC", ctypes.c_double * 10),
                ("_cf_CurrentsEUVSA_256",  ctypes.c_uint64 * 2),
                ("CurrentsEUVSA_256", ctypes.c_float * 30 * 11),
                ("_cf_CurrentsEUVSA_284",  ctypes.c_uint64 * 2),
                ("CurrentsEUVSA_284", ctypes.c_float * 30 * 5),
                ("_cf_CurrentsEUVSA_304",  ctypes.c_uint64 * 2),
                ("CurrentsEUVSA_304", ctypes.c_float * 30 * 6),
                ("_cf_CurrentsEUVSA_Dark",  ctypes.c_uint64 * 2),
                ("CurrentsEUVSA_Dark", ctypes.c_float * 30 * 2),
                ("_cf_CurrentsEUVSB_1175",  ctypes.c_uint64 * 2),
                ("CurrentsEUVSB_1175", ctypes.c_float * 30 * 5),
                ("_cf_CurrentsEUVSB_1216",  ctypes.c_uint64 * 2),
                ("CurrentsEUVSB_1216", ctypes.c_float * 30 * 6),
                ("_cf_CurrentsEUVSB_1335",  ctypes.c_uint64 * 2),
                ("CurrentsEUVSB_1335", ctypes.c_float * 30 * 5),
                ("_cf_CurrentsEUVSB_1405",  ctypes.c_uint64 * 2),
                ("CurrentsEUVSB_1405", ctypes.c_float * 30 * 6),
                ("_cf_CurrentsEUVSB_Dark",  ctypes.c_uint64 * 2),
                ("CurrentsEUVSB_Dark", ctypes.c_float * 30 * 2),
                ("_cf_SignalsEUVSC_hLine",  ctypes.c_uint64 * 2),
                ("SignalsEUVSC_hLine", ctypes.c_float * 10 * 10),
                ("_cf_SignalsEUVSC_kLine",  ctypes.c_uint64 * 2),
                ("SignalsEUVSC_kLine", ctypes.c_float * 10 * 10),
                ("_cf_IntegratedSignalsEUVSC_BlueWing",  ctypes.c_uint64),
                ("IntegratedSignalsEUVSC_BlueWing", ctypes.c_float * 10),
                ("_cf_IntegratedSignalsEUVSC_RedWing",  ctypes.c_uint64),
                ("IntegratedSignalsEUVSC_RedWing", ctypes.c_float * 10),
                ("_cf_IntegratedSignalsEUVSC_DarkMask",  ctypes.c_uint64),
                ("IntegratedSignalsEUVSC_DarkMask", ctypes.c_float * 10),
                ("Average_SPS_dispersion_angle",    ctypes.c_float),
                ("Average_SPS_cross_dispersion_angle",  ctypes.c_float),
                ("_cf_solar_array_current",    ctypes.c_uint64),
                ("solar_array_current", ctypes.c_uint16 * 4),
                ("SC_eclipse_flag", ctypes.c_uint8),
                ("euvscIntegrationTime", ctypes.c_float),
                ("_cf_euvscQualityFlags", ctypes.c_uint64),
                ("euvscQualityFlags", ctypes.c_uint32 * 10),
                ("Total_SPS_angles", ctypes.c_uint8),
                ("Total_valid_SPS_angle_pairs", ctypes.c_uint8),
                ("euvscActiveChannel", ctypes.c_uint8),
                ]

class EXIS_EUV_STRUCT_DO07_01(GRBStruct):
    _pack_ = 1
    _fields_ = [("_cf_irradianceSpectrum", ctypes.c_uint64),
                ("irradianceSpectrum", ctypes.c_float * 23),
                ("time",    ctypes.c_double),
                ("_cf_lowWavelength",  ctypes.c_uint64),
                ("lowWavelength",   ctypes.c_float * 23),
                ("_cf_highWavelength", ctypes.c_uint64),
                ("highWavelength",  ctypes.c_float * 23),
                ("EUV_CaseNumber",  ctypes.c_uint8),
                ("qualityFlags",    ctypes.c_uint64),
                ("quaternion_Q0",   ctypes.c_float),
                ("quaternion_Q1",   ctypes.c_float),
                ("quaternion_Q2",   ctypes.c_float),
                ("quaternion_Q3",   ctypes.c_float),
                ("ECEF_X", ctypes.c_float),
                ("ECEF_Y", ctypes.c_float),
                ("ECEF_Z", ctypes.c_float),
                ("au_factor",   ctypes.c_float),
                ("SC_yaw_flip_flag",    ctypes.c_uint8),
                ("nXRS",    ctypes.c_uint8),
                ("nGoodXRSA",   ctypes.c_uint8),
                ("nGoodXRSB",   ctypes.c_uint8),
                ("nEUVSA",  ctypes.c_uint8),
                ("nGood256",    ctypes.c_uint8),
                ("nGood284",    ctypes.c_uint8),
                ("nGood304",    ctypes.c_uint8),
                ("nEUVSB",  ctypes.c_uint8),
                ("nGood1175",   ctypes.c_uint8),
                ("nGood1216",   ctypes.c_uint8),
                ("nGood1335",   ctypes.c_uint8),
                ("nGood1405",   ctypes.c_uint8),
                ("nEUVSC",  ctypes.c_uint8),
                ("nGoodMg", ctypes.c_uint8),
                ("_cf_xrsQualityFlags",    ctypes.c_uint64),
                ("xrsQualityFlags", ctypes.c_uint32 * 30),
                ("_cf_euvsaQualityFlags",  ctypes.c_uint64),
                ("euvsaQualityFlags",   ctypes.c_uint32 * 30),
                ("_cf_euvsbQualityFlags",  ctypes.c_uint64),
                ("euvsbQualityFlags",   ctypes.c_uint32 * 30),
#                ("_cf_euvscQualityFlags",  ctypes.c_uint64),
#                ("euvscQualityFlags",   ctypes.c_uint32 * 15),
                ("euvsaAvgTemp",    ctypes.c_float),
                ("euvsbAvgTemp",    ctypes.c_float),
                ("euvsc1AvgTemp",   ctypes.c_float),
                ("euvsc2AvgTemp",   ctypes.c_float),
                ("avgIrradianceXRSA",   ctypes.c_float),
                ("avgIrradianceXRSB",   ctypes.c_float),
                ("avgIrradiance256",    ctypes.c_float),
                ("avgIrradiance284",    ctypes.c_float),
                ("avgIrradiance304",    ctypes.c_float),
                ("avgIrradiance1175",   ctypes.c_float),
                ("avgIrradiance1216",   ctypes.c_float),
                ("avgIrradiance1335",   ctypes.c_float),
                ("avgIrradiance1405",   ctypes.c_float),
                ("avgRatioMgExis",  ctypes.c_float),
                ("avgRatioMgNoaa",  ctypes.c_float),
                ("_cf_dailyIrradiance256",  ctypes.c_float), # NOTE: removed in the stream ("reserved"), set to _cf to be skipped 
                ("_cf_dailyIrradiance284",  ctypes.c_float), # NOTE: removed in the stream ("reserved"), set to _cf to be skipped
                ("_cf_dailyIrradiance304",  ctypes.c_float), # NOTE: removed in the stream ("reserved"), set to _cf to be skipped
                ("_cf_dailyIrradiance1175", ctypes.c_float), # NOTE: removed in the stream ("reserved"), set to _cf to be skipped
                ("_cf_dailyIrradiance1216", ctypes.c_float), # NOTE: removed in the stream ("reserved"), set to _cf to be skipped
                ("_cf_dailyIrradiance1335", ctypes.c_float), # NOTE: removed in the stream ("reserved"), set to _cf to be skipped
                ("_cf_dailyIrradiance1405", ctypes.c_float), # NOTE: removed in the stream ("reserved"), set to _cf to be skipped
                ("_cf_dailyRatioMgNoaa",    ctypes.c_float), # NOTE: removed in the stream ("reserved"), set to _cf to be skipped
                ("_cf_ObservationTimesEUVSAB",  ctypes.c_uint64),
                ("ObservationTimesEUVSAB", ctypes.c_double * 30),
                ("_cf_ObservationTimesEUVSC",  ctypes.c_uint64),
                ("ObservationTimesEUVSC", ctypes.c_double * 10),
                ("_cf_CurrentsEUVSA",  ctypes.c_uint64 * 2),
                ("CurrentsEUVSA", ctypes.c_float * 30 * 24),
                ("_cf_CurrentsEUVSB",  ctypes.c_uint64 * 2),
                ("CurrentsEUVSB", ctypes.c_float * 30 * 24),
                ("_cf_SignalsEUVSC_hLine",  ctypes.c_uint64 * 2),
                ("SignalsEUVSC_hLine", ctypes.c_float * 10 * 10),
                ("_cf_SignalsEUVSC_kLine",  ctypes.c_uint64 * 2),
                ("SignalsEUVSC_kLine", ctypes.c_float * 10 * 10),
                ("_cf_IntegratedSignalsEUVSC_BlueWing",  ctypes.c_uint64),
                ("IntegratedSignalsEUVSC_BlueWing", ctypes.c_float * 10),
                ("_cf_IntegratedSignalsEUVSC_RedWing",  ctypes.c_uint64),
                ("IntegratedSignalsEUVSC_RedWing", ctypes.c_float * 10),
                ("_cf_IntegratedSignalsEUVSC_DarkMask",  ctypes.c_uint64),
                ("IntegratedSignalsEUVSC_DarkMask", ctypes.c_float * 10),
                ("Average_SPS_dispersion_angle",    ctypes.c_float),
                ("Average_SPS_cross_dispersion_angle",  ctypes.c_float),
                ("_cf_solar_array_current",    ctypes.c_uint64),
                ("solar_array_current", ctypes.c_uint16 * 4),
                ("SC_eclipse_flag", ctypes.c_uint8),
                ("euvscIntegrationTime", ctypes.c_float),
                ("_cf_euvscQualityFlags", ctypes.c_uint64),
                ("euvscQualityFlags", ctypes.c_uint32 * 10),
                ("Total_SPS_angles", ctypes.c_uint8),
                ("Total_valid_SPS_angle_pairs", ctypes.c_uint8),
                ("euvscActiveChannel", ctypes.c_uint8),
                ]

# Table 7.4.2.5.1 Solar Flux: X-Ray Product Data


class EXIS_XRAY_STRUCT(GRBStruct):
    _pack_ = 1
    _fields_ = [("irradiance_xrsa1",    ctypes.c_float),
                ("irradiance_xrsa2",    ctypes.c_float),
                ("primary_xrsa",    ctypes.c_uint8),
                ("irradiance_xrsb1",    ctypes.c_float),
                ("irradiance_xrsb2",    ctypes.c_float),
                ("primary_xrsb",    ctypes.c_uint8),
                ("xrs_ratio",   ctypes.c_float),
                ("corrected_current_xrsa_1",    ctypes.c_float),
                ("corrected_current_xrsa_2",    ctypes.c_float),
                ("corrected_current_xrsa_3",    ctypes.c_float),
                ("corrected_current_xrsa_4",    ctypes.c_float),
                ("corrected_current_xrsb_1",    ctypes.c_float),
                ("corrected_current_xrsb_2",    ctypes.c_float),
                ("corrected_current_xrsb_3",    ctypes.c_float),
                ("corrected_current_xrsb_4",    ctypes.c_float),
                ("dispersion_angle",    ctypes.c_float),
                ("crossdispersion_angle",   ctypes.c_float),
                ("sc_power_side",   ctypes.c_uint8),
                ("exis_flight_model",   ctypes.c_uint8),
                ("exis_configuration_id",   ctypes.c_uint16),
                ("xrs_runctrlmd",   ctypes.c_uint8),
                ("integration_time",    ctypes.c_float),
                ("exs_sl_pwr_ena",  ctypes.c_uint8),
                ("asic1_temperature",   ctypes.c_float),
                ("asic2_temperature",   ctypes.c_float),
                ("invalid_flags",   ctypes.c_uint8),
                ("xrs_det_chg", ctypes.c_uint32),
                ("xrs_mode",    ctypes.c_uint8),
                ("_cf_sps_obs_time",   ctypes.c_uint64),
                ("sps_obs_time",    ctypes.c_double * 4),
                ("_cf_sps_int_time",   ctypes.c_uint64),
                ("sps_int_time",    ctypes.c_float * 4),
                ("_cf_sps_temperature",    ctypes.c_uint64),
                ("sps_temperature", ctypes.c_float * 4),
                ("_cf_sps_det_chg",    ctypes.c_uint64),
                ("sps_det_chg", ctypes.c_uint32 * 4),
                ("num_angle_pairs", ctypes.c_uint16),
                ("yaw_flip_flag",   ctypes.c_uint8),
                ("au_factor",   ctypes.c_float),
                ("quality_flags",   ctypes.c_uint32),
                ("time",    ctypes.c_double),
                ("packet_count",    ctypes.c_uint32),
                ("fov_unknown", ctypes.c_uint8),
                ("fov_eclipse", ctypes.c_uint8),
                ("fov_lunar_transit",   ctypes.c_uint8),
                ("fov_planet_transit",  ctypes.c_uint8),
                ("fov_off_point",   ctypes.c_uint8),
                ("quaternion_Q0",   ctypes.c_float),
                ("quaternion_Q1",   ctypes.c_float),
                ("quaternion_Q2",   ctypes.c_float),
                ("quaternion_Q3",   ctypes.c_float),
                ("ecef_X",  ctypes.c_float),
                ("ecef_Y",  ctypes.c_float),
                ("ecef_Z",  ctypes.c_float),
                ("_cf_solar_array_current", ctypes.c_uint64),
                ("solar_array_current", ctypes.c_uint16 * 4),
                ("SC_eclipse_flag", ctypes.c_uint8),
                ]

BAD_FIELDS = [
]

#print "DEBUG: sizeof EXIS_EUV_STRUCT:", ctypes.sizeof(EXIS_EUV_STRUCT)
#debugTotalSize = 0
#for field in EXIS_EUV_STRUCT._fields_:
#    print "DEBUG: sizeof", field[0], ctypes.sizeof(field[1]), "(total: ", debugTotalSize, ")"
#    debugTotalSize = debugTotalSize + ctypes.sizeof(field[1])


class EXIS(GRBDataset):
    track = False

    def __init__(self, h1, h2, hp):
        super(EXIS, self).__init__(h1, h2, hp)
        self.fields = {}
        self.ecount = 0
        self.xcount = 0

    def _add_metadata(self, h1, h2, hp, p):
        super(EXIS, self)._add_metadata(h1, h2, hp, p)
        self._sync_to_nc()

    def _add_data(self, h1, h2, hp, p):
        p = self._decompress(hp, p)
        LOG.info("Adding data payload of size: %d bytes" % len(p))
        if h1.apid in [0x381]:
            if len(p) == ctypes.sizeof(EXIS_EUV_STRUCT):
                data_struct = EXIS_EUV_STRUCT()
            elif len(p) == ctypes.sizeof(EXIS_EUV_STRUCT_DO07):
                data_struct = EXIS_EUV_STRUCT_DO07()
            elif len(p) == ctypes.sizeof(EXIS_EUV_STRUCT_DO07_01):
                data_struct = EXIS_EUV_STRUCT_DO07_01()
            else:
                LOG.error("sizeof EXIS_EUV_STRUCT: %d", ctypes.sizeof(EXIS_EUV_STRUCT))
                LOG.error("sizeof EXIS_EUV_STRUCT_DO07: %d", ctypes.sizeof(EXIS_EUV_STRUCT_DO07))
                LOG.error("sizeof EXIS_EUV_STRUCT_DO07_01: %d", ctypes.sizeof(EXIS_EUV_STRUCT_DO07_01))
                raise(RuntimeError, "EXIS EUV payload of size %d bytes does not match any known configurations" % (len(p)))
            self.ecount = self.ecount + 1
        elif h1.apid in [0x383]:
            data_struct = EXIS_XRAY_STRUCT()
            self.xcount = self.xcount + 1
        else:
            LOG.error("EXIS handler encountered unrecognized APID %s" %
                      hex(h1.apid))
            raise(NotImplementedError)

        if (ctypes.sizeof(data_struct) != len(p)):
            LOG.error("Size of APID %s Expected Payload (%d) != Actual Payload Size (%d)" % (hex(h1.apid), ctypes.sizeof(data_struct), len(p)))

        data_struct.receiveSome(p)

        for field_name, field_type in data_struct._fields_:
            if field_name.startswith("_cf_"):
                LOG.debug("skipping control field %s" % (field_name))
                continue

            if field_name in BAD_FIELDS:
                LOG.error(
                    "skipping field %s until test data complies with the PUG" % (field_name))
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

        if self.ncml:  # FIXME: should we be putting to the nc file before the metadata comes in?
            self._sync_to_nc()

    def _sync_to_nc(self):
        for field_name in self.fields.keys():
            LOG.info("Adding %s" % field_name)
            try:
                self.nc.variables[field_name][:] = self.fields[field_name][:]
            except Exception as e:
                LOG.error("Unexpected error putting %s to file: %s" %
                          (e, sys.exc_info()[0]))
        self.nc.sync()

