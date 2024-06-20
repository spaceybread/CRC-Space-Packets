#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Super basic interface to szip

Copyright © 2014-2017 University of Wisconsin Regents

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

from grbr.config import CSPP_GEO_GRBR_SZIP_LIB

import ctypes

import logging
LOG = logging.getLogger('GRB-R')


class SZ_com_t(ctypes.Structure):
    """
    from szlib.h...

    typedef struct SZ_com_t_s
      {
      int options_mask;
      int bits_per_pixel;
      int pixels_per_block;
      int pixels_per_scanline;
      } SZ_com_t;
    """

    _fields_ = [('options_mask',        ctypes.c_int),
                ('bits_per_pixel',      ctypes.c_int),
                ('pixels_per_block',    ctypes.c_int),
                ('pixels_per_scanline', ctypes.c_int)]

libsz = ctypes.CDLL(CSPP_GEO_GRBR_SZIP_LIB)
libsz_b2bdecompress = libsz.SZ_BufftoBuffDecompress
libsz_b2bdecompress.restype = ctypes.c_int
libsz_b2bdecompress.argtypes = [ctypes.c_void_p, ctypes.POINTER(
    ctypes.c_size_t), ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(SZ_com_t)]

SZ_RAW_OPTION_MASK = 128
SZ_LSB_OPTION_MASK = 8
SZ_NN_OPTION_MASK = 32


def decompress(buffer):
    # FIXME: Harris data has an extra 4 bytes of reserve, and is the only
    # thing to use szip at the moment
    buffer = buffer[4:]

    szct = SZ_com_t()
    szct.options_mask = SZ_RAW_OPTION_MASK | SZ_LSB_OPTION_MASK | SZ_NN_OPTION_MASK
    szct.bits_per_pixel = 8
    szct.pixels_per_block = 8
    szct.pixels_per_scanline = 8

    # FIXME: how large should our dest buffer be? can it blow up larger than
    # 8x?
    dest = ctypes.create_string_buffer(len(buffer) * 8)
    destLen = ctypes.c_size_t(len(dest))
    source = ctypes.create_string_buffer(
        buffer)  # FIXME: do we really need to make a copy? :(

    ret = libsz_b2bdecompress(ctypes.byref(dest), ctypes.byref(
        destLen), ctypes.byref(source), len(source), ctypes.byref(szct))
    if ret:
        LOG.error("szip return code: %d", ret)
    return dest.raw

# SZ_BufftoBuffCompress(void *dest, size_t *destLen, const void *source,
# size_t sourceLen, SZ_com_t *param)


"""
/// SZIP params
const int paramMask = SZ_RAW_OPTION_MASK | SZ_LSB_OPTION_MASK | SZ_NN_OPTION_MASK;

/// SZIP bits per pixel
const int paramBitsPerPixel = 8;

/// SZIP pixels per block
const int paramPixelsPerBlock = 8;

/// SZIP scanline
const int paramPixelsPerScanline = 8;

/// The maximum amount of data that can be compressed in bytes
const size_t MAX_SIZE = std::numeric_limits<uint32_t>::max();

/**
 * Builds a sz_stream
 *
 * @param anInputBuffer the input buffer for the sz_stream
 * @param anInputBufferSize the size of the input buffer
 * @param anOutputBuffer the output buffer for the sz_stream
 * @param anOutputSize the size of the output buffer
 * @param aNumPixels the number of pixels the stream will process
 */
sz_stream getStream(char*    anInputBuffer,
                    size_t   anInputBufferSize,
                    char*    anOutputBuffer,
                    size_t   anOutputSize,
                    uint32_t aNumPixels)
{
   sz_stream stream;

   stream.options_mask = paramMask;
   stream.hidden = 0;
   stream.image_pixels = aNumPixels;
   stream.bits_per_pixel = paramBitsPerPixel;
   stream.pixels_per_block = paramPixelsPerBlock;
   stream.pixels_per_scanline = paramPixelsPerScanline;
   stream.next_in = anInputBuffer;
   stream.avail_in = anInputBufferSize;
   stream.total_in = 0;

   stream.next_out = anOutputBuffer;
   stream.avail_out = anOutputSize;
   stream.total_out = 0;

   return stream;
}
"""
