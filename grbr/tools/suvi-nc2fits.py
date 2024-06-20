#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utility for converting SUVI netCDF4 files to FITS.

astropy FITS documentation: http://astropy.readthedocs.org/en/latest/io/fits/

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


import os, sys
from netCDF4 import Dataset
from astropy.io import fits
import numpy as np
import argparse
import re
control_chars = ''.join(map(chr, list(range(0,32)) + list(range(127,160))))
control_char_re = re.compile('[%s]' % re.escape(control_chars))

from datetime import timedelta, datetime

import logging
LOG = logging.getLogger('GRB-R')


def epoch2datestring(seconds_since_epoch, epoch=datetime(2000,1,1,12,0,0)):
    if seconds_since_epoch < 0:
        LOG.warning("encountered negative seconds since epoch")
        return seconds_since_epoch
    td_sse = timedelta(seconds=seconds_since_epoch)
    utc_unadjusted = td_sse + epoch
    return utc_unadjusted.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] # the PDA files chop off the microseconds so let's do the same

def convert(ncname, fitsname):
    nc = Dataset(ncname)
    rad = nc.variables['RAD']
    rad.set_auto_maskandscale(False)
    dqf = nc.variables['DQF']
    dqf.set_auto_maskandscale(False)

    radhdr = fits.Header()
    dqfhdr = fits.Header()

    def from_netcdf_vattr(v, a):
        try:
            var = nc.variables[v]
            return getattr(var, a)
        except:
            LOG.warning("variable attribute %s.%s not present" % (v, a))
            return

    def from_netcdf_attr(a):
        try:
            return getattr(nc, a)
        except AttributeError:
            LOG.warning("attribute %s not present" % (a))
            return



    def from_netcdf_var(v):
        try:
            var = nc.variables[v]
        except KeyError:
            LOG.warning("variable %s not present" % (v))
            return

        var.set_auto_maskandscale(False)
        if var.dtype == np.dtype("S1"):
            return control_char_re.sub('', var[:].tobytes().decode('utf-8')) # note some strings had additional null characters, which the FITS library didn't like
        elif var.dtype in [np.dtype("float32"), np.dtype("float64")]:
            # FIXME: this should be handled with more precision
            return float(str(var[0]))
        elif var.dtype in [np.dtype("int8"), np.dtype("int16"), np.dtype("int32")]:
            return int(var[0])
        else:
            LOG.warning("var: %s dtype: %s is not handled explicitly!" % (v, var.dtype))
            return var[0]

    # headers defined in PUG V3 "Table 5.2.1.5.2 Data Fields for FITS Format"
    radhdr.set("SIMPLE", "T")
    radhdr.set("BITPIX", 16)
    radhdr.set("NAXIS", 2)
    radhdr.set("NAXIS1", 1280)
    radhdr.set("NAXIS2", 1280)
    radhdr.set("EXTEND", "T")
    radhdr.set("EXTNAME", "DATA")
    radhdr.set("EXTVER", 1)
    radhdr.set("UUID", "not provided via GRB")
    radhdr.set("CRPIX1", from_netcdf_var("CRPIX1"))
    radhdr.set("CRPIX2", from_netcdf_var("CRPIX2"))
    radhdr.set("CDELT1", from_netcdf_var("CDELT1"))
    radhdr.set("CDELT2", from_netcdf_var("CDELT2"))
    radhdr.set("DIAM_SUN", from_netcdf_var("DIAM_SUN"))
    radhdr.set("CUNIT1", from_netcdf_var("CUNIT1"))
    radhdr.set("CUNIT2", from_netcdf_var("CUNIT2"))
    radhdr.set("ORIENT", from_netcdf_var("ORIENT"))
    radhdr.set("CROTA", from_netcdf_var("CROTA"))
    radhdr.set("SOLAR_B0", from_netcdf_var("SOLAR_B0"))
    radhdr.set("PC1_1", from_netcdf_var("PC1_1"))
    radhdr.set("PC1_2", from_netcdf_var("PC1_2"))
    radhdr.set("PC2_1", from_netcdf_var("PC2_1"))
    radhdr.set("PC2_2", from_netcdf_var("PC2_2"))
    radhdr.set("CSYER1", from_netcdf_var("CSYER1"))
    radhdr.set("CSYER2", from_netcdf_var("CSYER2"))
    radhdr.set("WCSNAME", from_netcdf_var("WCSNAME"))
    radhdr.set("CTYPE1", from_netcdf_var("CTYPE1"))
    radhdr.set("CTYPE2", from_netcdf_var("CTYPE2"))
    radhdr.set("CRVAL1", from_netcdf_var("CRVAL1"))
    radhdr.set("CRVAL2", from_netcdf_var("CRVAL2"))
    radhdr.set("LONPOLE", from_netcdf_var("LONPOLE"))
    radhdr.set("TIMESYS", from_netcdf_var("TIMESYS"))
    radhdr.set("DATE-OBS", epoch2datestring(from_netcdf_var("DATE-OBS")))
    radhdr.set("DATE-END", epoch2datestring(from_netcdf_var("DATE-END")))
    radhdr.set("CMD_EXP", from_netcdf_var("CMD_EXP"))
    radhdr.set("EXPTIME", from_netcdf_var("EXPTIME"))
    radhdr.set("OBSGEO-X", from_netcdf_var("OBSGEO-X"))
    radhdr.set("OBSGEO-Y", from_netcdf_var("OBSGEO-Y"))
    radhdr.set("OBSGEO-Z", from_netcdf_var("OBSGEO-Z"))
    radhdr.set("DSUN_OBS", from_netcdf_var("DSUN_OBS"))
    radhdr.set("OBJECT", from_netcdf_var("OBJECT"))
    radhdr.set("SCI_OBJ", from_netcdf_var("SCI_OBJ"))
    radhdr.set("WAVELNTH", from_netcdf_var("WAVELNTH"))
    radhdr.set("WAVEUNIT", from_netcdf_var("WAVEUNIT"))
    radhdr.set("GOOD_PIX", from_netcdf_var("GOOD_PIX"))
    radhdr.set("FIX_PIX", from_netcdf_var("FIX_PIX"))
    radhdr.set("SAT_PIX", from_netcdf_var("SAT_PIX"))
    radhdr.set("MISS_PIX", from_netcdf_var("MISS_PIX"))
    radhdr.set("IMGTII", from_netcdf_var("IMGTII"))
    radhdr.set("IMGTIR", from_netcdf_var("IMGTIR"))
    radhdr.set("IMG_MIN", from_netcdf_var("IMG_MIN"))
    radhdr.set("IMG_MAX", from_netcdf_var("IMG_MAX"))
    radhdr.set("IMG_MEAN", from_netcdf_var("IMG_MEAN"))
    radhdr.set("IMG_SDEV", from_netcdf_var("IMG_SDEV"))
    radhdr.set("EFF_AREA", from_netcdf_var("EFF_AREA"))
    radhdr.set("APSELPOS", from_netcdf_var("APSELPOS"))
    radhdr.set("INSTRESP", from_netcdf_var("INSTRESP"))
    radhdr.set("PHOT_ENG", from_netcdf_var("PHOT_ENG"))
    radhdr.set("RSUN",     from_netcdf_var("RSUN"))
    radhdr.set("HGLT_OBS", from_netcdf_var("HGLT_OBS"))
    radhdr.set("HGLN_OBS", from_netcdf_var("HGLN_OBS"))
    radhdr.set("HEEX_OBS", from_netcdf_var("HEEX_OBS"))
    radhdr.set("HEEY_OBS", from_netcdf_var("HEEY_OBS"))
    radhdr.set("HEEZ_OBS", from_netcdf_var("HEEZ_OBS"))
    radhdr.set("IMSENUMB", from_netcdf_var("IMSENUMB"))
    radhdr.set("FILTPOS1", from_netcdf_var("FILTPOS1"))
    radhdr.set("FILTPOS2", from_netcdf_var("FILTPOS2"))
    radhdr.set("FILTER1", from_netcdf_var("FILTER1"))
    radhdr.set("FILTER2", from_netcdf_var("FILTER2"))
    radhdr.set("YAW_FLIP", from_netcdf_var("YAW_FLIP"))
    radhdr.set("CCD_READ", from_netcdf_var("CCD_READ"))
    radhdr.set("ECLIPSE", from_netcdf_var("ECLIPSE"))
    radhdr.set("CONTAMIN", from_netcdf_var("CONTAMIN"))
    radhdr.set("CONT_FLG", from_netcdf_var("CONT_FLG"))
    radhdr.set("DATE-BKE", epoch2datestring(from_netcdf_var("DATE-BKE")))
    radhdr.set("DER_SNR", from_netcdf_var("DER_SNR"))
    radhdr.set("SAT_THR", from_netcdf_var("SAT_THR"))
    radhdr.set("CCD_BIAS", from_netcdf_var("CCD_BIAS"))
    radhdr.set("CCD_TMP1", from_netcdf_var("CCD_TMP1"))
    radhdr.set("CCD_TMP2", from_netcdf_var("CCD_TMP2"))
    radhdr.set("DATE-DFM", epoch2datestring(from_netcdf_var("DATE-DFM")))
    radhdr.set("NDFRAMES", from_netcdf_var("NDFRAMES"))
    radhdr.set("DATE-DF0", epoch2datestring(from_netcdf_var("DATE-DF0")))
    radhdr.set("DATE-DF1", epoch2datestring(from_netcdf_var("DATE-DF1")))
    radhdr.set("DATE-DF2", epoch2datestring(from_netcdf_var("DATE-DF2")))
    radhdr.set("DATE-DF3", epoch2datestring(from_netcdf_var("DATE-DF3")))
    radhdr.set("DATE-DF4", epoch2datestring(from_netcdf_var("DATE-DF4")))
    radhdr.set("DATE-DF5", epoch2datestring(from_netcdf_var("DATE-DF5")))
    radhdr.set("DATE-DF6", epoch2datestring(from_netcdf_var("DATE-DF6")))
    radhdr.set("DATE-DF7", epoch2datestring(from_netcdf_var("DATE-DF7")))
    radhdr.set("DATE-DF8", epoch2datestring(from_netcdf_var("DATE-DF8")))
    radhdr.set("DATE-DF9", epoch2datestring(from_netcdf_var("DATE-DF9")))
    radhdr.set("SOLCURR1", from_netcdf_var("SOLCURR1"))
    radhdr.set("SOLCURR2", from_netcdf_var("SOLCURR2"))
    radhdr.set("SOLCURR3", from_netcdf_var("SOLCURR3"))
    radhdr.set("SOLCURR4", from_netcdf_var("SOLCURR4"))
    radhdr.set("BUNIT",    from_netcdf_vattr("RAD", "units"))
    radhdr.set("PCTL0ERR", from_netcdf_var("PCTL0ERR"))
    radhdr.set("FILENAME", from_netcdf_attr("dataset_name"))
    radhdr.set("NAMEAUTH", from_netcdf_attr("naming_authority"))
    radhdr.set("LONGSTRN", "OGIP 1.0")
    radhdr.set("LUT_NAME", from_netcdf_attr("LUT_Filenames"))
    radhdr.set("ORIGIN", from_netcdf_attr("institution"))
    radhdr.set("PROJECT", from_netcdf_attr("project"))
    radhdr.set("ISO_META", from_netcdf_attr("iso_series_metadata_id"))
    radhdr.set("KEYVOCAB", from_netcdf_attr("keywords_vocabulary"))
    radhdr.set("TITLE", from_netcdf_attr("title"))
    radhdr.set("SUMMARY", from_netcdf_attr("summary"))
    radhdr.set("LICENSE", from_netcdf_attr("license"))
    radhdr.set("KEYWORDS", from_netcdf_attr("keywords"))
    radhdr.set("TELESCOP", from_netcdf_attr("platform_ID"))
    radhdr.set("INSTRUME", from_netcdf_attr("instrument_type"))
    radhdr.set("INST_ID", from_netcdf_attr("instrument_id"))
    # FIXME: "serial number of the instrument" - where do we get this? n.b.: does not appear to be set in Harris' FITS files either
#    radhdr.set("INST_ID", "unknown")
    radhdr.set("LEVEL", from_netcdf_attr("processing_level"))
    radhdr.set("ORB_SLOT", from_netcdf_attr("orbital_slot"))
    radhdr.set("DATE", from_netcdf_attr("date_created")[:-1]) # strip off the trailing "Z"
    radhdr.set("CREATOR", from_netcdf_attr("algorithm_version"))
    radhdr.set("PRODSITE", from_netcdf_attr("production_site"))
    radhdr.set("PROD_ENV", from_netcdf_attr("production_environment"))
    radhdr.set("DATA_SRC", from_netcdf_attr("production_data_source"))
    radhdr.set("BLANK", -32768)

    dqfhdr.set("XTENSION", "IMAGE")
    dqfhdr.set("BITPIX", 8)
    dqfhdr.set("NAXIS", 2)
    dqfhdr.set("NAXIS1", 1280)
    dqfhdr.set("NAXIS2", 1280)
    dqfhdr.set("PCOUNT", 0)
    dqfhdr.set("GCOUNT", 1)
    dqfhdr.set("EXTNAME", "DQF")
    dqfhdr.set("EXTVER", 1)
    dqfhdr.set("FLAGVAL", str(dqf.FITS_flag_values))
    dqfhdr.set("LONGSTRN", "OGIP 1.0")
    dqfhdr.set("FLAGMEAN", str(dqf.flag_meanings))

    radhdu = fits.PrimaryHDU(data=rad[:], header=radhdr, uint=False, do_not_scale_image_data=True, scale_back=False)

    # NOTE: :we do the float(str(...)) wrapping below to avoid this issue, as the astropy fits library converts to float behind the scenes and was adding false precision
    # >>> np.float32(0.0009919)
    # 0.0009919
    # >>> float(np.float32(0.0009919))
    # 0.000991899985820055
    # >>> float(str(np.float32(0.0009919)))
    # 0.0009919

    # FIXME: this is a bit of a hack, since BSCALE and BZERO get deleted by the above PrimaryHDU constructor when we do provide them???
    radhdu._header.set("BSCALE", float(str(rad.scale_factor)))
    radhdu._header.set("BZERO", float(str(rad.add_offset)))

    dqfhdu = fits.ImageHDU(data=dqf[:].astype(np.uint8), header=dqfhdr, uint=False, do_not_scale_image_data=True, scale_back=False, name="DQF")
    hdulist = fits.HDUList([radhdu, dqfhdu])

    radhdu.add_checksum()
    radhdu.add_datasum()
    dqfhdu.add_checksum()
    dqfhdu.add_datasum()

    hdulist.writeto(fitsname)


def _setup_argparse():
    parser = argparse.ArgumentParser(
        description="Utility for converting a SUVI netCDF4 file to FITS.")

    # Required arguments:
    parser.add_argument('netCDF4 file', help='a single SUVI netCDF4 files')

    parser.add_argument('-o', '--output', dest="output", action="store", default=0, help="the output FITS filename")

    # Optional arguments:
    parser.add_argument('-v', '--verbose', dest='verbosity', action="count", default=0,
                        help='each occurrence increases verbosity through ERROR, WARNING, INFO, DEBUG')

    return parser


if __name__ == '__main__':
    # Get input args
    parser = _setup_argparse()
    args = parser.parse_args()

    # Setup logging
    levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    verbosity = min(args.verbosity, len(levels) - 1)
    logging.basicConfig(level=levels[verbosity])

    # Process input
    ncname = getattr(args, "netCDF4 file")
    if os.path.exists(ncname):
        if not args.output:
            fitsname = os.path.splitext(ncname)[0] + ".fits"
        else:
            fitsname = args.output
        convert(ncname, fitsname)
    else:
        LOG.error("File does not exist: %s" % input)
