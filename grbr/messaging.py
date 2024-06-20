#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module containing structs & functions for inter-process messaging

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
from time import sleep

# FIXME: what should this be? currently 512 - 32 (PIPE_BUF - offset)
MAX_FILE_LENGTH = 480


class UsefulStruct(ctypes.Structure):

    def send(self):
        return buffer(self)[:]

    def receiveSome(self, bytes):
        fit = min(len(bytes), ctypes.sizeof(self))
        ctypes.memmove(ctypes.addressof(self), bytes, fit)


class FILE_OFFSET(UsefulStruct):
    _pack_ = 1
    _fields_ = [
        ('offset',   ctypes.c_uint32),
        ('filename', ctypes.c_char * MAX_FILE_LENGTH),
    ]


def send_file_offset(fifopath, infile, start):
    fo = FILE_OFFSET()
    if len(infile) > MAX_FILE_LENGTH:
        raise(RuntimeError, "infile too large")
    fo.filename = infile
    fo.offset = start

    fifo = open(fifopath, 'w')
    fifo.write(fo.send())
    fifo.close()


def receive_file_offset(fifopath):
    msgsize = ctypes.sizeof(FILE_OFFSET)
    fifo = open(fifopath, 'rb')
    while True:
        stuff = fifo.read(msgsize)
        if stuff == "":
            sleep(5)  # FIXME: this sleep is gross :(
            continue
        fo = FILE_OFFSET()
        fo.receiveSome(stuff)
        yield fo
