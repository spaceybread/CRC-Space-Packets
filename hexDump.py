import binascii
with open(input(), 'rb') as f:
    for chunk in iter(lambda: f.read(131120), b''):
        print(binascii.hexlify(chunk))
    

