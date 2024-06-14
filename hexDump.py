import binascii
import zlib
import sys

def b(x):
    return int(bin(x)[2:])

def li(n):
    return list(map(int,str(b(n))))


a = None

with open(input(), 'rb') as f:
    for chunk in iter(lambda: f.read(131120), b''):
        a = binascii.hexlify(chunk)

packet = a
print(packet)
poly  = 4374732215

print(hex(zlib.crc32(packet)))
