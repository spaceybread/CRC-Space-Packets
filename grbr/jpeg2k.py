#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Super basic interface to jpeg2000

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

#import numpy as np
#import cStringIO

import glymur
import tempfile
import os
from grbr.config import CSPP_GEO_GRBR_TMP

def decompress(stream):

    # FIXME: i don't like putting this to a file :(
    temp = tempfile.NamedTemporaryFile(delete=False, prefix="cspp-grb-", dir=CSPP_GEO_GRBR_TMP, suffix=".jp2")
    temp.write(stream)
    temp.close()
    try:
        jp2 = glymur.Jp2k(temp.name)
        data = jp2[:]
    finally:
        os.unlink(temp.name)
    return data

    """
# FIXME: pillow seems to freeze randomly? glymur wants a file to open? zzz gonna have to write our own
  from PIL import Image as PILI
  pic = PILI.open(cStringIO.StringIO(stream))
  data = pic.getdata()
  adata = np.array(data, dtype=np.uint16)
  adata = adata.reshape(data.size, order='F')
  return np.flipud(np.rot90(adata))
  """
