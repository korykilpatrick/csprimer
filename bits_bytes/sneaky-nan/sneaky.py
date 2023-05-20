# https://en.wikipedia.org/wiki/NaN#Encoding
# represent NaN with exponent fields all filled with 1s and a nonzero num in significand field
# signed bit doesnt matter
#  s111 1111 1xxx xxxx xxxx xxxx xxxx xxxx

import struct

def conceal(x):
    # load string into NaN payload
    bits = ''.join(format(ord(c), '08b') for c in x)
    print(int(bits) | 0b11111111000000000000000000000000)
    return 0b11111111000000000000000000000000 | int(''.join(format(ord(c), '08b') for c in x))

def reveal(x):
    pass

print(conceal('hi'))