def makeBig(poly):
    bigTable = [0] * 256
    crc = 32768 # needs to be changed, idk what this is actually supposed to be


    i = 1
    while i < 256:
        if crc & 32768:
            crc = (crc << 1) ^ poly
        else:
            crc = (crc << 1)
    
        for j in range(i):
            bigTable[i + j] = crc ^ bigTable[j]
        i = i << 1

    for i in range(256):
        if i % 16 == 0:
            print()
        print(hex(bigTable[i]), end= " ")

def makeSmall(poly):
    smallTable = [0] * 256
    crc = 1 # I think this one is just 1 regardless of context
    
    i = 128
    while i > 0:
        if crc & 1:
            crc = (crc >> 1) ^ poly
        else:
            crc = crc >> 1
        
        for j in range(0, 255, 2):
            smallTable[i ^ j] = crc ^ smallTable[j]
        
        i = i >> 1
    
    for i in range(256):
        if i % 16 == 0:
            print()
        print(hex(smallTable[i]), end= " ")

makeBig(4374732215)
