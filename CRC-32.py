def c32(arr, table):
    # table in this context is the lookup table
    # arr is an array of bytes
    
    crc32 = 4294967295
    
    for i in range(len(arr)):
        idx = (crc32 ^ arr[i]) & 255
        crc32 = (crc32 >> 8) ^ table[idx]
    
    crc32 = crc32 ^ 4294967295
    return crc32

