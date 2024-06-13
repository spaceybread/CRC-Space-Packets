def make(poly):
    bigTable = [0] * 256
    crc = 32768


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

for i in range(600000, 655370):
    make(i)
    print()
    print("=" * 64, " ", end = "")
    print(i)
    print()
    input()
