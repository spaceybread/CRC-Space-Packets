#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tools for reconstructing SEISS

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

# 7.5.1 - Energy Heavy Ions Product
# EHIS

class SEISS_EHIS_STRUCT(GRBStruct):
    _pack_ = 1
    _fields_ = [("_cf_H5MinuteDifferentialFluxes", ctypes.c_uint64),
                ("H5MinuteDifferentialFluxes", ctypes.c_float * 5),
                ("_cf_H5MinuteDifferentialFluxStatErrors", ctypes.c_uint64),
                ("H5MinuteDifferentialFluxStatErrors", ctypes.c_float * 5),
                ("_cf_H5MinuteDifferentialFluxInstErrors", ctypes.c_uint64),
                ("H5MinuteDifferentialFluxInstErrors", ctypes.c_float * 5),
                ("_cf_H5MinuteDifferentialEnergyBounds", ctypes.c_uint64 * 2),
                ("H5MinuteDifferentialEnergyBounds", ctypes.c_float * 2 * 5),
                ("_cf_He5MinuteDifferentialFluxes", ctypes.c_uint64),
                ("He5MinuteDifferentialFluxes", ctypes.c_float * 5),
                ("_cf_He5MinuteDifferentialFluxStatErrors", ctypes.c_uint64),
                ("He5MinuteDifferentialFluxStatErrors", ctypes.c_float * 5),
                ("_cf_He5MinuteDifferentialFluxInstErrors", ctypes.c_uint64),
                ("He5MinuteDifferentialFluxInstErrors", ctypes.c_float * 5),
                ("_cf_He5MinuteDifferentialEnergyBounds", ctypes.c_uint64 * 2),
                ("He5MinuteDifferentialEnergyBounds", ctypes.c_float * 2 * 5),
                ("_cf_CNO5MinuteDifferentialFluxes", ctypes.c_uint64),
                ("CNO5MinuteDifferentialFluxes", ctypes.c_float * 5),
                ("_cf_CNO5MinuteDifferentialFluxStatErrorsBounds", ctypes.c_uint64 * 2),
                ("CNO5MinuteDifferentialFluxStatErrorsBounds", ctypes.c_float * 2 * 5),
                ("_cf_CNO5MinuteDifferentialEnergyBounds", ctypes.c_uint64 * 2),
                ("CNO5MinuteDifferentialEnergyBounds", ctypes.c_float * 2 * 5),
                ("_cf_CNO5MinuteDifferentialFluxInstErrors", ctypes.c_uint64),
                ("CNO5MinuteDifferentialFluxInstErrors", ctypes.c_float * 5),
                ("_cf_NeS5MinuteDifferentialFluxes", ctypes.c_uint64),
                ("NeS5MinuteDifferentialFluxes", ctypes.c_float * 5),
                ("_cf_NeS5MinuteDifferentialFluxStatErrorsBounds", ctypes.c_uint64 * 2),
                ("NeS5MinuteDifferentialFluxStatErrorsBounds", ctypes.c_float * 2 * 5),
                ("_cf_NeS5MinuteDifferentialEnergyBounds", ctypes.c_uint64 * 2),
                ("NeS5MinuteDifferentialEnergyBounds", ctypes.c_float * 2 * 5),
                ("_cf_NeS5MinuteDifferentialFluxInstErrors", ctypes.c_uint64),
                ("NeS5MinuteDifferentialFluxInstErrors", ctypes.c_float * 5),
                ("_cf_ClNi5MinuteDifferentialFluxes", ctypes.c_uint64),
                ("ClNi5MinuteDifferentialFluxes", ctypes.c_float * 5),
                ("_cf_ClNi5MinuteDifferentialFluxStatErrorsBounds", ctypes.c_uint64 * 2),
                ("ClNi5MinuteDifferentialFluxStatErrorsBounds", ctypes.c_float * 2 * 5),
                ("_cf_ClNi5MinuteDifferentialEnergyBounds", ctypes.c_uint64 * 2),
                ("ClNi5MinuteDifferentialEnergyBounds", ctypes.c_float * 2 * 5),
                ("_cf_ClNi5MinuteDifferentialFluxInstErrors", ctypes.c_uint64),
                ("ClNi5MinuteDifferentialFluxInstErrors", ctypes.c_float * 5),
                ("_cf_BeCu5MinuteDifferentialFluxes", ctypes.c_uint64 * 2),
                ("BeCu5MinuteDifferentialFluxes", ctypes.c_float * 5 * 26),
                ("_cf_BeCu5MinuteDifferentialFluxStatErrorsBounds", ctypes.c_uint64 * 3),
                ("BeCu5MinuteDifferentialFluxStatErrorsBounds",
                 ctypes.c_float * 5 * 26 * 2),
                ("_cf_BeCu5MinuteDifferentialEnergyBounds", ctypes.c_uint64 * 3),
                ("BeCu5MinuteDifferentialEnergyBounds", ctypes.c_float * 5 * 26 * 2),
                ("_cf_BeCu5MinuteDifferentialFluxInstErrors", ctypes.c_uint64 * 2),
                ("BeCu5MinuteDifferentialFluxInstErrors", ctypes.c_float * 5 * 26),
                ("_cf_H5MinuteDifferentialFluxDQFs", ctypes.c_uint64),
                ("H5MinuteDifferentialFluxDQFs", ctypes.c_uint8 * 5),
                ("_cf_He5MinuteDifferentialFluxDQFs", ctypes.c_uint64),
                ("He5MinuteDifferentialFluxDQFs", ctypes.c_uint8 * 5),
                ("_cf_CNO5MinuteDifferentialFluxDQFs", ctypes.c_uint64),
                ("CNO5MinuteDifferentialFluxDQFs", ctypes.c_uint8 * 5),
                ("_cf_NeS5MinuteDifferentialFluxDQFs", ctypes.c_uint64),
                ("NeS5MinuteDifferentialFluxDQFs", ctypes.c_uint8 * 5),
                ("_cf_ClNi5MinuteDifferentialFluxDQFs", ctypes.c_uint64),
                ("ClNi5MinuteDifferentialFluxDQFs", ctypes.c_uint8 * 5),
                ("_cf_BeCu5MinuteDifferentialFluxDQFs", ctypes.c_uint64 * 2),
                ("BeCu5MinuteDifferentialFluxDQFs", ctypes.c_uint8 * 5 * 26),
                ("_cf_Overall_Validity_Flag", ctypes.c_uint64),
                ("Overall_Validity_Flag", ctypes.c_uint8 * 5),
                ("Process_Together_Flag", ctypes.c_uint8),
                ("_cf_L1a_EngData_Flag", ctypes.c_uint64),
                ("L1a_EngData_Flag", ctypes.c_uint8 * 5),
                ("_cf_L1a_PECData_Flag", ctypes.c_uint64),
                ("L1a_PECData_Flag", ctypes.c_uint8 * 5),
                ("_cf_L1a_HCRData_Flag", ctypes.c_uint64),
                ("L1a_HCRData_Flag", ctypes.c_uint8 * 5),
                ("_cf_L1a_ELFData_Flag", ctypes.c_uint64),
                ("L1a_ELFData_Flag", ctypes.c_uint8 * 5),
                ("_cf_HFR_Flag", ctypes.c_uint64),
                ("HFR_Flag", ctypes.c_uint8 * 5),
                ("_cf_IFC_Flag", ctypes.c_uint64),
                ("IFC_Flag", ctypes.c_uint8 * 5),
                ("_cf_SCC_Flag", ctypes.c_uint64),
                ("SCC_Flag", ctypes.c_uint8 * 5),
                ("N_blocks", ctypes.c_uint8),
                ("_cf_Instrument_Mode", ctypes.c_uint64),
                ("Instrument_Mode", ctypes.c_uint8 * 5),
                ("Instrument_Serial_Number", ctypes.c_uint8),
                ("_cf_PEC_StartStopTime", ctypes.c_uint64),
                ("PEC_StartStopTime", ctypes.c_double * 2),
                ("_cf_HCR_StartStop_Time", ctypes.c_uint64),
                ("HCR_StartStop_Time", ctypes.c_double * 2),
                ("_cf_ELF_StartStopTime", ctypes.c_uint64),
                ("ELF_StartStopTime", ctypes.c_double * 2),
                ("quaternion_Q0", ctypes.c_float),
                ("quaternion_Q1", ctypes.c_float),
                ("quaternion_Q2", ctypes.c_float),
                ("quaternion_Q3", ctypes.c_float),
                ("ECEF_X", ctypes.c_float),
                ("ECEF_Y", ctypes.c_float),
                ("ECEF_Z", ctypes.c_float),
                ("yaw_flip_flag", ctypes.c_uint8),
                ("eclipse_flag", ctypes.c_uint8),
                ("_cf_solar_array_current", ctypes.c_uint64),
                ("solar_array_current", ctypes.c_uint16 * 4),
                ]

class SEISS_EHIS_STRUCT_DO080100(GRBStruct):
    _pack_ = 1
    _fields_ = [("_cf_H5MinuteDifferentialFluxes", ctypes.c_uint64),
                ("H5MinuteDifferentialFluxes", ctypes.c_float * 5),
                ("_cf_H5MinuteDifferentialFluxStatErrors", ctypes.c_uint64),
                ("H5MinuteDifferentialFluxStatErrors", ctypes.c_float * 5),
                ("_cf_H5MinuteDifferentialFluxInstErrors", ctypes.c_uint64),
                ("H5MinuteDifferentialFluxInstErrors", ctypes.c_float * 5),
                ("_cf_H5MinuteDifferentialEnergyBounds", ctypes.c_uint64 * 2),
                ("H5MinuteDifferentialEnergyBounds", ctypes.c_float * 2 * 5),
                ("_cf_He5MinuteDifferentialFluxes", ctypes.c_uint64),
                ("He5MinuteDifferentialFluxes", ctypes.c_float * 5),
                ("_cf_He5MinuteDifferentialFluxStatErrors", ctypes.c_uint64),
                ("He5MinuteDifferentialFluxStatErrors", ctypes.c_float * 5),
                ("_cf_He5MinuteDifferentialFluxInstErrors", ctypes.c_uint64),
                ("He5MinuteDifferentialFluxInstErrors", ctypes.c_float * 5),
                ("_cf_He5MinuteDifferentialEnergyBounds", ctypes.c_uint64 * 2),
                ("He5MinuteDifferentialEnergyBounds", ctypes.c_float * 2 * 5),
                ("_cf_CNO5MinuteDifferentialFluxes", ctypes.c_uint64),
                ("CNO5MinuteDifferentialFluxes", ctypes.c_float * 5),
                ("_cf_CNO5MinuteDifferentialFluxStatErrorsBounds", ctypes.c_uint64 * 2),
                ("CNO5MinuteDifferentialFluxStatErrorsBounds", ctypes.c_float * 2 * 5),
                ("_cf_CNO5MinuteDifferentialEnergyBounds", ctypes.c_uint64 * 2),
                ("CNO5MinuteDifferentialEnergyBounds", ctypes.c_float * 2 * 5),
                ("_cf_CNO5MinuteDifferentialFluxInstErrors", ctypes.c_uint64),
                ("CNO5MinuteDifferentialFluxInstErrors", ctypes.c_float * 5),
                ("_cf_NeS5MinuteDifferentialFluxes", ctypes.c_uint64),
                ("NeS5MinuteDifferentialFluxes", ctypes.c_float * 5),
                ("_cf_NeS5MinuteDifferentialFluxStatErrorsBounds", ctypes.c_uint64 * 2),
                ("NeS5MinuteDifferentialFluxStatErrorsBounds", ctypes.c_float * 2 * 5),
                ("_cf_NeS5MinuteDifferentialEnergyBounds", ctypes.c_uint64 * 2),
                ("NeS5MinuteDifferentialEnergyBounds", ctypes.c_float * 2 * 5),
                ("_cf_NeS5MinuteDifferentialFluxInstErrors", ctypes.c_uint64),
                ("NeS5MinuteDifferentialFluxInstErrors", ctypes.c_float * 5),
                ("_cf_ClNi5MinuteDifferentialFluxes", ctypes.c_uint64),
                ("ClNi5MinuteDifferentialFluxes", ctypes.c_float * 5),
                ("_cf_ClNi5MinuteDifferentialFluxStatErrorsBounds", ctypes.c_uint64 * 2),
                ("ClNi5MinuteDifferentialFluxStatErrorsBounds", ctypes.c_float * 2 * 5),
                ("_cf_ClNi5MinuteDifferentialEnergyBounds", ctypes.c_uint64 * 2),
                ("ClNi5MinuteDifferentialEnergyBounds", ctypes.c_float * 2 * 5),
                ("_cf_ClNi5MinuteDifferentialFluxInstErrors", ctypes.c_uint64),
                ("ClNi5MinuteDifferentialFluxInstErrors", ctypes.c_float * 5),
                ("_cf_BeCu5MinuteDifferentialFluxes", ctypes.c_uint64 * 2),
                ("BeCu5MinuteDifferentialFluxes", ctypes.c_float * 5 * 26),
                ("_cf_BeCu5MinuteDifferentialFluxStatErrorsBounds", ctypes.c_uint64 * 3),
                ("BeCu5MinuteDifferentialFluxStatErrorsBounds",
                 ctypes.c_float * 5 * 26 * 2),
                ("_cf_BeCu5MinuteDifferentialEnergyBounds", ctypes.c_uint64 * 3),
                ("BeCu5MinuteDifferentialEnergyBounds", ctypes.c_float * 5 * 26 * 2),
                ("_cf_BeCu5MinuteDifferentialFluxInstErrors", ctypes.c_uint64 * 2),
                ("BeCu5MinuteDifferentialFluxInstErrors", ctypes.c_float * 5 * 26),
                ("_cf_H5MinuteDifferentialFluxDQFs", ctypes.c_uint64),
                ("H5MinuteDifferentialFluxDQFs", ctypes.c_uint8 * 5),
                ("_cf_He5MinuteDifferentialFluxDQFs", ctypes.c_uint64),
                ("He5MinuteDifferentialFluxDQFs", ctypes.c_uint8 * 5),
                ("_cf_CNO5MinuteDifferentialFluxDQFs", ctypes.c_uint64),
                ("CNO5MinuteDifferentialFluxDQFs", ctypes.c_uint8 * 5),
                ("_cf_NeS5MinuteDifferentialFluxDQFs", ctypes.c_uint64),
                ("NeS5MinuteDifferentialFluxDQFs", ctypes.c_uint8 * 5),
                ("_cf_ClNi5MinuteDifferentialFluxDQFs", ctypes.c_uint64),
                ("ClNi5MinuteDifferentialFluxDQFs", ctypes.c_uint8 * 5),
                ("_cf_BeCu5MinuteDifferentialFluxDQFs", ctypes.c_uint64 * 2),
                ("BeCu5MinuteDifferentialFluxDQFs", ctypes.c_uint8 * 5 * 26),
                ("_cf_Overall_Validity_Flag", ctypes.c_uint64),
                ("Overall_Validity_Flag", ctypes.c_uint8 * 5),
                ("Process_Together_Flag", ctypes.c_uint8),
                ("_cf_L1a_EngData_Flag", ctypes.c_uint64),
                ("L1a_EngData_Flag", ctypes.c_uint8 * 5),
                ("_cf_L1a_PECData_Flag", ctypes.c_uint64),
                ("L1a_PECData_Flag", ctypes.c_uint8 * 5),
                ("_cf_L1a_HCRData_Flag", ctypes.c_uint64),
                ("L1a_HCRData_Flag", ctypes.c_uint8 * 5),
                ("_cf_L1a_ELFData_Flag", ctypes.c_uint64),
                ("L1a_ELFData_Flag", ctypes.c_uint8 * 5),
                ("_cf_HFR_Flag", ctypes.c_uint64),
                ("HFR_Flag", ctypes.c_uint8 * 5),
                ("_cf_IFC_Flag", ctypes.c_uint64),
                ("IFC_Flag", ctypes.c_uint8 * 5),
                ("_cf_SCC_Flag", ctypes.c_uint64),
                ("SCC_Flag", ctypes.c_uint8 * 5),
                ("N_blocks", ctypes.c_uint8),
                ("_cf_Instrument_Mode", ctypes.c_uint64),
                ("Instrument_Mode", ctypes.c_uint8 * 5),
                ("Instrument_Serial_Number", ctypes.c_uint8),
                ("_cf_HCR_StartStop_Time", ctypes.c_uint64),
                ("HCR_StartStop_Time", ctypes.c_double * 2),
                ("_cf_PEC_StartStopTime", ctypes.c_uint64),
                ("PEC_StartStopTime", ctypes.c_double * 2),
                ("_cf_ELF_StartStopTime", ctypes.c_uint64),
                ("ELF_StartStopTime", ctypes.c_double * 2),
                ("quaternion_Q0", ctypes.c_float),
                ("quaternion_Q1", ctypes.c_float),
                ("quaternion_Q2", ctypes.c_float),
                ("quaternion_Q3", ctypes.c_float),
                ("ECEF_X", ctypes.c_float),
                ("ECEF_Y", ctypes.c_float),
                ("ECEF_Z", ctypes.c_float),
                ("yaw_flip_flag", ctypes.c_uint8),
                ("eclipse_flag", ctypes.c_uint8),
                ("_cf_solar_array_current", ctypes.c_uint64),
                ("solar_array_current", ctypes.c_uint16 * 4),
                ]

# 7.5.2 - Magnetospheric Electrons and Protons: Low Energy Product
# MPSL

class SEISS_MPSL_STRUCT(GRBStruct):
    _pack_ = 1
    _fields_ = [("_cf_DiffElectronFluxes", ctypes.c_uint64 * 2),
                ("DiffElectronFluxes", ctypes.c_float * 15 * 14),
                ("_cf_DiffElectronFluxDQFs", ctypes.c_uint64 * 2),
                ("DiffElectronFluxDQFs", ctypes.c_uint8 * 15 * 14),
                ("_cf_DiffIonFluxes", ctypes.c_uint64 * 2),
                ("DiffIonFluxes", ctypes.c_float * 15 * 14),
                ("_cf_DiffIonFluxDQFs", ctypes.c_uint64 * 2),
                ("DiffIonFluxDQFs", ctypes.c_uint8 * 15 * 14),
                ("_cf_DiffElectronUncertainties", ctypes.c_uint64 * 2),
                ("DiffElectronUncertainties", ctypes.c_float * 15 * 14),
                ("_cf_DiffIonUncertainties", ctypes.c_uint64 * 2),
                ("DiffIonUncertainties", ctypes.c_float * 15 * 14),
                ("L1a_EngData_Flag", ctypes.c_uint8),
                ("L1a_IonData_Flag", ctypes.c_uint8),
                ("L1a_EleData_Flag", ctypes.c_uint8),
                ("L1b_Processing_Flag", ctypes.c_uint8),
                ("N_blocks", ctypes.c_uint8),
                ("Instrument_Mode", ctypes.c_uint8),
                ("Instrument_Serial_Number", ctypes.c_uint8),
                ("L1a_SciData_TimeStamp", ctypes.c_double),
                ("quaternion_Q0", ctypes.c_float),
                ("quaternion_Q1", ctypes.c_float),
                ("quaternion_Q2", ctypes.c_float),
                ("quaternion_Q3", ctypes.c_float),
                ("ECEF_X", ctypes.c_float),
                ("ECEF_Y", ctypes.c_float),
                ("ECEF_Z", ctypes.c_float),
                ("yaw_flip_flag", ctypes.c_uint8),
                ("eclipse_flag", ctypes.c_uint8),
                ("_cf_solar_array_current", ctypes.c_uint64),
                ("solar_array_current", ctypes.c_uint16 * 4),
                ]

# 7.5.3 - Magnetospheric Electrons and Protons: Medium and High Energy Product
# MPSH

class SEISS_MPSH_STRUCT(GRBStruct):
    _pack_ = 1
    _fields_ = [("_cf_DiffElectronFluxes", ctypes.c_uint64 * 2),
                ("DiffElectronFluxes", ctypes.c_float * 10 * 5),
                ("_cf_IntgElectronFluxes", ctypes.c_uint64),
                ("IntgElectronFluxes", ctypes.c_float * 5),
                ("_cf_DiffProtonFluxes", ctypes.c_uint64 * 2),
                ("DiffProtonFluxes", ctypes.c_float * 11 * 5),
                ("_cf_DiffElectronUncertainties", ctypes.c_uint64 * 2),
                ("DiffElectronUncertainties", ctypes.c_float * 10 * 5),
                ("_cf_IntgElectronUncertainties", ctypes.c_uint64),
                ("IntgElectronUncertainties", ctypes.c_float * 5),
                ("_cf_DiffProtonUncertainties", ctypes.c_uint64 * 2),
                ("DiffProtonUncertainties", ctypes.c_float * 11 * 5),
                ("_cf_DiffElectronFluxDQFs", ctypes.c_uint64 * 2),
                ("DiffElectronFluxDQFs", ctypes.c_uint8 * 10 * 5),
                ("_cf_DiffProtonFluxDQFs", ctypes.c_uint64 * 2),
                ("DiffProtonFluxDQFs", ctypes.c_uint8 * 11 * 5),
                ("_cf_IntgElectronFluxDQFs", ctypes.c_uint64),
                ("IntgElectronFluxDQFs", ctypes.c_uint8 * 5),
                ("Dos1_HiLetDose", ctypes.c_float),
                ("Dos1_HiLetDqf", ctypes.c_uint8),
                ("Dos2_HiLetDose", ctypes.c_float),
                ("Dos2_HiLetDqf", ctypes.c_uint8),
                ("Dos1_LoLetDose", ctypes.c_float),
                ("Dos1_LoLetDqf", ctypes.c_uint8),
                ("Dos2_LoLetDose", ctypes.c_float),
                ("Dos2_LoLetDqf", ctypes.c_uint8),
                ("L1a_EngData_Flag", ctypes.c_uint8),
                ("L1a_ProtonData_Flag", ctypes.c_uint8),
                ("L1a_EleData_Flag", ctypes.c_uint8),
                ("L1a_DosData_Flag", ctypes.c_uint8),
                ("L1b_Processing_Flag", ctypes.c_uint8),
                ("N_blocks", ctypes.c_uint8),
                ("Instrument_Mode", ctypes.c_uint8),
                ("Instrument_Serial_Number", ctypes.c_uint8),
                ("L1a_SciData_TimeStamp", ctypes.c_double),
                ("quaternion_Q0", ctypes.c_float),
                ("quaternion_Q1", ctypes.c_float),
                ("quaternion_Q2", ctypes.c_float),
                ("quaternion_Q3", ctypes.c_float),
                ("ECEF_X", ctypes.c_float),
                ("ECEF_Y", ctypes.c_float),
                ("ECEF_Z", ctypes.c_float),
                ("yaw_flip_flag", ctypes.c_uint8),
                ("eclipse_flag", ctypes.c_uint8),
                ("_cf_solar_array_current", ctypes.c_uint64),
                ("solar_array_current", ctypes.c_uint16 * 4),
                ]

# 7.5.4 - Solar and Galactic Protons Product
# SGPS

class SEISS_SGPS_STRUCT(GRBStruct):
    _pack_ = 1
    _fields_ = [("_cf_T1_DifferentialProtonFluxes", ctypes.c_uint64 * 2),
                ("T1_DifferentialProtonFluxes", ctypes.c_float * 2 * 6),
                ("_cf_T1_DifferentialProtonFluxUncertainties", ctypes.c_uint64 * 2),
                ("T1_DifferentialProtonFluxUncertainties", ctypes.c_float * 2 * 6),
                ("_cf_T1_DifferentialProtonFluxDQFs", ctypes.c_uint64 * 2),
                ("T1_DifferentialProtonFluxDQFs", ctypes.c_uint8 * 2 * 6),
                ("_cf_T2_DifferentialProtonFluxes", ctypes.c_uint64 * 2),
                ("T2_DifferentialProtonFluxes", ctypes.c_float * 2 * 2),
                ("_cf_T2_DifferentialProtonFluxUncertainties", ctypes.c_uint64 * 2),
                ("T2_DifferentialProtonFluxUncertainties", ctypes.c_float * 2 * 2),
                ("_cf_T2_DifferentialProtonFluxDQFs", ctypes.c_uint64 * 2),
                ("T2_DifferentialProtonFluxDQFs", ctypes.c_uint8 * 2 * 2),
                ("_cf_T3_DifferentialProtonFluxes", ctypes.c_uint64 * 2),
                ("T3_DifferentialProtonFluxes", ctypes.c_float * 2 * 5),
                ("_cf_T3_DifferentialProtonFluxUncertainties", ctypes.c_uint64 * 2),
                ("T3_DifferentialProtonFluxUncertainties", ctypes.c_float * 2 * 5),
                ("_cf_T3_DifferentialProtonFluxDQFs", ctypes.c_uint64 * 2),
                ("T3_DifferentialProtonFluxDQFs", ctypes.c_uint8 * 2 * 5),
                ("_cf_T3P11_IntegralProtonFlux", ctypes.c_uint64),
                ("T3P11_IntegralProtonFlux", ctypes.c_float * 2),
                ("_cf_T3P11_IntegralProtonFluxUncertainties", ctypes.c_uint64),
                ("T3P11_IntegralProtonFluxUncertainties", ctypes.c_float * 2),
                ("_cf_T3P11_IntegralProtonFluxDQFs", ctypes.c_uint64),
                ("T3P11_IntegralProtonFluxDQFs", ctypes.c_uint8 * 2),
                ("_cf_L1a_EngData_Flag", ctypes.c_uint64),
                ("L1a_EngData_Flag", ctypes.c_uint8 * 2),
                ("_cf_L1a_SciData_Flag", ctypes.c_uint64),
                ("L1a_SciData_Flag", ctypes.c_uint8 * 2),
                ("L1b_Processing_Flag", ctypes.c_uint8),
                ("_cf_N_blocks", ctypes.c_uint64),
                ("N_blocks", ctypes.c_uint8 * 2),
                ("_cf_Instrument_Mode", ctypes.c_uint64),
                ("Instrument_Mode", ctypes.c_uint8 * 2),
                ("_cf_Instrument_Serial_Number", ctypes.c_uint64), # note: PUG RevE lists this as uint8
                ("Instrument_Serial_Number", ctypes.c_uint8 * 2),
                ("_cf_Diff31_Logic_Flags", ctypes.c_uint64 * 2),
                ("Diff31_Logic_Flags", ctypes.c_uint8 * 2 * 3),
                ("_cf_L1a_SciData_TimeStamp", ctypes.c_uint64),
                ("L1a_SciData_TimeStamp", ctypes.c_double * 2),
                ("quaternion_Q0", ctypes.c_float),
                ("quaternion_Q1", ctypes.c_float),
                ("quaternion_Q2", ctypes.c_float),
                ("quaternion_Q3", ctypes.c_float),
                ("ECEF_X", ctypes.c_float),
                ("ECEF_Y", ctypes.c_float),
                ("ECEF_Z", ctypes.c_float),
                ("yaw_flip_flag", ctypes.c_uint8),
                ("eclipse_flag", ctypes.c_uint8),
                ("_cf_solar_array_current", ctypes.c_uint64),
                ("solar_array_current", ctypes.c_uint16 * 4),
                ("_cf_sgps_telemetry_time", ctypes.c_uint64),
                ("sgps_telemetry_time", ctypes.c_double * 2),
                ("_cf_sgps_sensor_temperature", ctypes.c_uint64 * 2),
                ("sgps_sensor_temperature", ctypes.c_float * 2 * 4),
                ]

#print "DEBUG: sizeof SEISS_EHIS_STRUCT:", ctypes.sizeof(SEISS_EHIS_STRUCT)
#print "DEBUG: sizeof SEISS_MPSL_STRUCT:", ctypes.sizeof(SEISS_MPSL_STRUCT)
#print "DEBUG: sizeof SEISS_MPSH_STRUCT:", ctypes.sizeof(SEISS_MPSH_STRUCT)
#print "DEBUG: sizeof SEISS_SGPS_STRUCT:", ctypes.sizeof(SEISS_SGPS_STRUCT)

BAD_FIELDS = [
]


class SEISS(GRBDataset):
    track = False

    def __init__(self, h1, h2, hp):
        super(SEISS, self).__init__(h1, h2, hp)
        self.fields = {}
        self.hcount = 0
        self.lcount = 0
        self.mcount = 0
        self.scount = 0

    def _add_metadata(self, h1, h2, hp, p):
        super(SEISS, self)._add_metadata(h1, h2, hp, p)
        self._sync_to_nc()

    def _add_data(self, h1, h2, hp, p):
        p = self._decompress(hp, p)
        LOG.info("Adding data payload of size: %d" % len(p))
        if h1.apid in [0x400, 0x401]:
            data_struct = SEISS_EHIS_STRUCT_DO080100() # FIXME: same payload size means we can't easily flip between the two
            self.hcount = self.hcount + 1
        elif h1.apid in [0x410, 0x411]:
            data_struct = SEISS_MPSL_STRUCT()
            self.lcount = self.lcount + 1
        elif h1.apid in [0x420, 0x421]:
            data_struct = SEISS_MPSH_STRUCT()
            self.mcount = self.mcount + 1
        elif h1.apid in [0x430, 0x431]:
            data_struct = SEISS_SGPS_STRUCT()
            self.scount = self.scount + 1
        else:
            raise(NotImplementedError)

        if len(p) != ctypes.sizeof(data_struct):
            raise(LOG.error("SEISS payload of size %d bytes does not match the expected configuration" % (len(p))))

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

        if self.ncml:
            self._sync_to_nc()

    def _sync_to_nc(self):
        for field_name in self.fields.keys():
            LOG.info("Adding %s" % field_name)
            try:
                self.nc.variables[field_name][:] = self.fields[field_name][:]
            except Exception as e:
                LOG.error("Unexpected error: %s" % e)
        self.nc.sync()

