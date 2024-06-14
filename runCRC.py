import os

def table():
    a = []
    for i in range(256):
        k = i
        for j in range(8):
            if k & 1:
                k ^= 0x1db710640
            k >>= 1
        a.append(k)
    return a

def hash(buf):
    crc = 0 ^ 0xffffffff
    for k in buf:
        crc = (crc >> 8) ^ table[(crc & 0xff) ^ k]
    return crc ^ 0xffffffff

table = table()

os.system('cp packet991 processing')

file = open('processing', 'br+')
file.seek(-4, os.SEEK_END)
out = file.read()
outIn = int.from_bytes(out, byteorder='little')
file.close()

file = open('processing', 'br+')
file.seek(-4, os.SEEK_END)
file.truncate()
file.close()

file = open('processing', 'br+')
data = file.read()
file.close()

print(hex(hash(data)), int(hex(hash(data)), 16) == 1469400536, outIn)
