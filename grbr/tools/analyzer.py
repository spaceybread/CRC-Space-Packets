#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utility to parse the packet stream, save apid vs. order (time),
plot a dot graph with x-axis time to see what kind of order the
packets come in.

Usage example: `python analyzer.py -p 15m.png 15m.ccsds`

Copyright © 2014-2018 University of Wisconsin Regents

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
GNU General Public License for more details.
"""

import argparse
import mmap
from collections import namedtuple
from matplotlib import pyplot

from netCDF4 import Dataset

from sp_structs import parse_packet
from cache import datetime_from_hp

import logging
LOG = logging.getLogger(__name__)

nfo = namedtuple('nfo', ['apid', 'size', 'date'])


def _print_results(nfos, checkout=False):
    print("n apid size date")
    for i, r in enumerate(nfos):
        if not checkout or r.date is not None:
            print(i, hex(r.apid), r.size, r.date)


def _plot_results(nfos, filename):
    # matplotlib setup before we can do any real work
    # [u'dark_background', u'bmh', u'grayscale', u'ggplot', u'fivethirtyeight']
    pyplot.style.use('dark_background')
    fig = pyplot.gcf()
    pyplot.title("GRB Bundle Analysis - APID vs. Packet #")
    fig.gca().set_autoscale_on(False)
    fig.set_size_inches(90, 70)

    # set up data & axis
    x = [n + 1 for n in range(len(nfos))]
    y = [nfo.apid for nfo in nfos]
#    size = [nfo.size for nfo in nfos] # seems super huge...
    print("count", "min", min(x), "max", max(x))
    print("apid", "min", hex(min(y)), "max", hex(max(y)))

    # apids at top of range were skewing, just use the full range documented
    # in the PUG
    pyplot.ylim([0, 0x7ff])
    pyplot.xlim([min(x), max(x)])

    # get y-axis labels
    apid_labels = [
        ('ABI FD Meta', 0x108),
        ('ABI FD Img', 0x118),
        ('ABI CONUS Meta', 0x128),
        ('ABI CONUS Img', 0x138),
        ('ABI Meso1 Meta', 0x148),
        ('ABI Meso1 Img', 0x158),
        ('ABI Meso2 Meta', 0x168),
        ('ABI Meso2 Img', 0x178),
        ('ABI Mode 4 Meta', 0x188),
        ('ABI Mode 4 Img', 0x198),
        ('GLM', 0x300),
        ('EXIS', 0x380),
        ('SEISS', 0x400),
        ('SEISS', 0x410),
        ('SEISS', 0x420),
        ('SEISS', 0x430),
        ('SUVI', 0x480),
        ('MAG', 0x500),
        ('GRB INFO', 0x580),
    ]
    instr_labels, instr_apids = zip(*apid_labels)

    # plot & save
    # , s=size) seems super huge?
    pyplot.scatter(x, y, c=y, marker='1', cmap=pyplot.get_cmap('Pastel1'))
    pyplot.tick_params('y', labelsize=10)
    pyplot.yticks(instr_apids, instr_labels)
    pyplot.savefig(filename, dpi=100, bbox_inches='tight')


def analyze(file_list):
    nfos = []
    for filename in file_list:
        LOG.info("Analyzing: %s" % (filename))
        if ".nc" in filename:
            nfos += analyze_netcdf(filename)
        elif ".ccsds" in filename:
            nfos += analyze_ccsds(filename)
        else:
            raise(RuntimeError("unrecognized file: %s" % (filename)))
    return nfos


def analyze_netcdf(netcdf_filename):
    nc = Dataset(netcdf_filename, 'r')
    packets = nc.variables['grb_space_packet_data'][:]
#    offsets = nc.variables['offset_to_packet'][:]
#    sizes = nc.variables['size_of_packet'][:]
    pbuffer = packets.tobytes()
    return _buffer2nfo(pbuffer)


def analyze_ccsds(ccsds_filename):
    ccsds = open(ccsds_filename, 'rb')
    mmmap = mmap.mmap(ccsds.fileno(), 0, access=mmap.ACCESS_READ)
    return _buffer2nfo(mmmap)


def _buffer2nfo(abuffer):
    nfos = []
    start = 0
    while start < len(abuffer):
        LOG.debug("scan @ index: %d" % (start))
        h1, h2, hp, _ = parse_packet(abuffer, start)
        end = start + h1.data_length + 7
        try:
            date = datetime_from_hp(hp)
        except:
            date = None
        nfos.append(nfo(h1.apid, h1.data_length, date))
        start = end
    return nfos


def _setup_argparse():
    parser = argparse.ArgumentParser(description=__doc__)

    # Required arguments:
    parser.add_argument('input', nargs=argparse.REMAINDER,
                        help='any number of CCSDS packet bundle files, in the order they should be analyzed')

    # Optional arguments:
    parser.add_argument('-c', '--checkout', dest='checkout', action='store_true',
                        default=False, help='for checking out a dataset, print only header packets')
    parser.add_argument('-p', '--plot', dest='plot', action='store', default=False,
                        help="make a plot of the results, save to given filename")
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

    nfos = analyze(args.input)

    if args.plot:
        _plot_results(nfos, args.plot)
    else:
        _print_results(nfos, checkout=args.checkout)
