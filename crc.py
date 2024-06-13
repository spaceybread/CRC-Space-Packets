def b(x):
    return int(bin(x)[2:])

def li(n):
    return list(map(int,str(b(n))))

hexPack = "48656c6c6f20576f726c642120546869732069732061206c6f6e6720737472696e672074686174204920776f756c64206c696b656420746f207465737420435243206f6e2e2049207468696e6b206974206d69676874206c6f6e6720656e6f756768206e6f77"



packet = int(bin(int(hexPack, 16)).zfill(8)[2:], 2)
poly  = 65537

# 1557394236 -> check sum
# 1320065244 -> calc with 31
# 2965741524 -> calc with 32

import sys
sys.set_int_max_str_digits(65537)

print(b(packet))
print(b(poly))

m = li(packet)
l = len(m)
p = li(poly)

for i in range(len(p) - 1):
    m.append(0)

i = 0
while True:
    if m[i] == 1:
        for j in range(len(p)):
            m[i + j] = m[i + j] ^ p[j]
    
        #for x in m:
        #    print(x, end="")
        #print()
        
        flag = True
        for k in range(l):
            if m[k] == 1:
                flag = False
        
        if flag:
            break
    i += 1

for id in range(l, len(m)):
    print(m[id], end="")

print()
