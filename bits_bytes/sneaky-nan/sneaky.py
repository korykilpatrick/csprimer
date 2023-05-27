# https://en.wikipedia.storg/wiki/NaN#Encoding
# represent NaN with exponent fields all filled with 1s and a nonzero num in significand field
# signed bit doesnt matter for nan (diff between neg and pos inf)

import struct

def conceal(x):
    # load string into NaN significand bits
    assert len(x) <= 6, "Can't encode more than 6 bytes!"
    
    float_inf = bytes([0b01111111, 0b11110000, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    # theres probably a better way to do this that doesn't involve pad + zip?
    x_padded_bytes = b'\x00' * (8 - len(x)) + bytes(x, 'utf-8')
    result = bytes([a | b for a, b in zip(float_inf, x_padded_bytes)])
    return struct.unpack('>d', result)[0]

def extract(x):
    # extract string from significand bits
    return struct.pack('>d', x)[2:].decode('utf-8')

x = conceal('oh yea')
print(type(x))
print(x)
print(x+5)
print(x / 2)
x += 3
print(x)
print(extract(x))
msg = 'oh yea'
assert msg == extract(conceal(msg))