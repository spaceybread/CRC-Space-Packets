#!/usr/bin/env python
# encoding: utf-8
"""
NcML -> NetCDF code, heavily borrowed from davidh's polar2grid

Copyright © 2017-2018 University of Wisconsin Regents

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

import sys
import logging
import numpy
from netCDF4 import Dataset
from bs4 import BeautifulSoup

log = logging.getLogger('GRB-R')

def unistr(s):
    return s.encode('utf8')

_types = {
    "float": numpy.float32,
    "int": numpy.int32,
    "uint": numpy.uint32,
    None: unistr,
    "string": unistr,
    "short": numpy.short,
    "ushort": numpy.ushort,
    "double": numpy.double,
    "long": numpy.int64,
    "ulong": numpy.uint64,
    "ubyte": numpy.uint8,
    "byte": numpy.int8
}

_type_str = {
    "float": "f4",
    "int": "i4",
    "uint": "u4",
    "double": "f8",
    "byte": "i1",
    "ubyte": "u1",
    "short": "i2",
    "ushort": "u2",
    "string": "c",
    "char": "c",
    "long": "i8",
    "ulong": "u8",
    "String": "c",  # FIXME: DOE SEISS 0x420 has this?
}


def _process_dimension(dimension, nc):
    """
    Parent should always be nc, right? If not, the below will fail...
    """
    if dimension.get('name') not in nc.dimensions:
        new_dim = nc.createDimension(dimension.get('name'), dimension.get('length') and int(dimension.get('length')))


def _process_values(values, parent):

    if values.get("start") is not None and values.get("increment") is not None:
        start = int(values.get("start"))
        stop = int(len(parent))
        increment = int(values.get("increment"))
        parent.set_auto_maskandscale(False)
        # this will scale if we don't turn off scaling above
        parent[:] = range(start, stop, increment)
        return

    if values.text is None:
        return

    if values.text == "n/a" and parent.dtype != numpy.dtype('c'):
        return

    txt = values.text.strip().split(" ")
    # we have to handle strings differently to split them character-wise
    # properly
    if parent.dtype == numpy.dtype('c'):
        val = numpy.chararray(parent.shape)
        # FIXME: this is really gross and can undoubtedly be improved, but
        # works for now...
        if len(parent.shape) == 1:
            # FIXME: why does looping like this work but not assigning the
            # whole thing at once?
            for i in range(len(txt[0])):
                val[i] = txt[0][i]
        elif len(parent.shape) == 2:
            try:
                for i in range(len(txt)):
                    toassign = list(txt[i])
                    toassign = toassign + [''] * (len(val[i]) - len(toassign))
                    val[i][:] = toassign
            except:
                # import pdb; pdb.set_trace()
                pass
        else:
            raise(RuntimeError("something we've never seen before"))
    else:
        val = numpy.array(txt, dtype=parent.dtype)
        if len(val) == 1:
            val = val[0]
#    print "DEBUG: parent name:", parent.name
#    print "DEBUG: parent:", parent
#    print "DEBUG: val:", val
#    import pdb; pdb.set_trace()
    if parent.name in [u'lowWavelengthLines', u'highWavelengthLines']:
        parent[0,:] = val
    else:
        parent[:] = val


def _process_attribute(attribute, parent):
    # _FillValue needs to be set at variable creation
    if attribute.get('name') == '_FillValue':
        return

    val = attribute.get("value")

    # this is a better fix than using splittable attrs I think
    # FIXME: apparently long_name isn't getting a type? are there others?
    if attribute.get("type") == None and attribute.get('name') == 'long_name':
        setattr(parent, attribute.get("name"), val)
    elif not attribute.get("type") == 'string':
        val = val.split(" ")

    try:
        setattr(parent, attribute.get("name"), _types[attribute.get("type")](val))
    except:
        log.error("could not cast: %s (%s), data likely doesn't match the specified type: %s" % (
            attribute.get("name"), attribute.get("value"), attribute.get("type")))


def _process_variable(variable, nc, compression=1):
    fill = None

    for attr in variable.findChildren('attribute'):
        if attr.get("name") == "_FillValue":
            fill = _types[attr.get("type")](attr.get("value"))

    if variable.get("shape"): # FIXME: why are we doing this again?
        dims = tuple(variable.get("shape").split(" "))

        while "" in dims:
            dims = list(dims)
            dims.remove("")
            dims = tuple(dims)

        # FIXME: NCML typo for MAG
        # FIXME: do we still need this?
        if "number_of_samples_per_report" in dims:
            dims = list(dims)
            dims[dims.index("number_of_samples_per_report")
                 ] = "number_samples_per_report"
            dims = tuple(dims)

        try:
            if variable.get("name") not in nc.variables:
                new_var = nc.createVariable(variable.get("name"), _type_str[
                                            variable.get("type")], dims, fill_value=fill,
                                            zlib=True, complevel=compression)
            else:
                new_var = nc.variables[variable.get("name")]

        except ValueError:
            log.error("could not add variable %s to the file, likely an invalid dimension in the ncml" % (
                variable.get("name")))
            return None
    else:
        if variable.get("name") not in nc.variables:
            new_var = nc.createVariable(variable.get("name"), _type_str[
                                        variable.get("type")], fill_value=fill,
                                        zlib=True, complevel=compression)
        else:
            new_var = nc.variables[variable.get("name")]

    # now add all the variable's attributes
    for attribute in variable.findChildren('attribute'):
        _process_attribute(attribute, new_var)

    # now add the actual data to the variable, if it's defined via NCML
    for values in variable.findChildren('values'):
        _process_values(values, new_var)


def create_nc_from_ncml(nc_filename, ncml_filename, format="NETCDF4"):
    """Take a NCML file and create a NetCDF file filled with the attributes
    and variables listed in the NCML file.
    """
    nc = Dataset(nc_filename, 'w', format=format)
    update_nc_from_ncml(nc, ncml_filename, format=format)


def update_nc_from_ncml(nc, ncml_filename, compression=1, format="NETCDF4"):
    ncml = open(ncml_filename, 'r')
    soup = BeautifulSoup(ncml, "xml")

    # top level of soup is just the naming XML & unidata namespace lines;
    # root of our netcdf file lives a level below
    for root in soup.children:
        for d in root.find_all("dimension", recursive=False):
            _process_dimension(d, nc)
        for a in root.find_all("attribute", recursive=False):
            _process_attribute(a, nc)
        for v in root.find_all("variable", recursive=False):
            _process_variable(v, nc, compression=compression)

    ncml.close()

    return nc


def main():
    logging.basicConfig(level=logging.DEBUG)
    return create_nc_from_ncml(sys.argv[2], sys.argv[1])

if __name__ == "__main__":
    sys.exit(main())
