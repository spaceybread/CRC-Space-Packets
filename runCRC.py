import os

# Creates a lookup table for CRC checks
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

# Computes the checksum of the file
def hash(buf, table):
    crc = 0 ^ 0xffffffff
    for k in buf:
        crc = (crc >> 8) ^ table[(crc & 0xff) ^ k]
    return crc ^ 0xffffffff

def decode(fileName, tab):
    # To avoid modifying the original space packet, I just make a copy and operate on that copy
    command = "cp " + fileName + " processing"
    os.system(command)
    
    # Read the checksum and process it
    file = open('processing', 'br+')
    file.seek(-4, os.SEEK_END)
    out = file.read()
    outIn = int.from_bytes(out, byteorder='big')
    file.close()
    
    # Strip the checksum
    file = open('processing', 'br+')
    file.seek(-4, os.SEEK_END)
    file.truncate()
    file.close()
    
    # Read the stripped file
    file = open('processing', 'br+')
    data = file.read()
    file.close()
    
    # For debugging, get the checksum and if it passes
    
    if int(hex(hash(data, tab)), 16) != outIn:
        print("Replace checksum with:", hex(hash(data, tab)))
    else:
        print(hex(hash(data, tab)), int(hex(hash(data, tab)), 16), int(hex(hash(data, tab)), 16) == outIn)
    
    # For future use, if it returns False, the packet fails the data integrity check
    # True otherwise
    return int(hex(hash(data, tab)), 16) == outIn

if __name__ == "__main__":
    
    # This is just for testing on the few packets that I have
    samples = ['packet991', 'packet992', 'packet993', 'packet994', 'packet995', 'packet996', 'packet997', 'packet998', 'packet999', 'packetFFF', 'packetGGG']
    
    tab = table()
    for sample in samples:
        decode('samples/' + sample, tab)
