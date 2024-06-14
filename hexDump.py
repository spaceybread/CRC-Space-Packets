import binascii

def b(x):
    return int(bin(x)[2:])

def li(n):
    return list(map(int,str(b(n))))


a = None

with open(input(), 'rb') as f:
    for chunk in iter(lambda: f.read(131120), b''):
        a = binascii.hexlify(chunk)

packet = int(a, 16)
print(packet)
poly  = 4374732215

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

