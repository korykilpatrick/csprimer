# Implementing protobuf varint encoding as detailed https://protobuf.dev/programming-guides/encoding/#varints
import struct 
import cProfile

def encode(number):
    out = []
    while True:
        chunk = number & 0b01111111
        number >>= 7
        out.append(chunk)
        if number > 0:
            out[-1] |= 0b10000000
        else:
            break
        
    return bytes(out)

"""real    25m25.770s
user    25m14.747s
sys     0m4.254s"""
def decode1(varint):
    # varint is a byte string in big endian.
    # we need to drop the MSB from each byte and read the number as little endian
    out = 0
    i = 0
    while i < len(varint):
        out |= (varint[i] & 0b01111111) << (7 * i)
        i += 1
    return out

"""real    27m9.209s
user    27m7.254s
sys     0m1.670s
"""
def decode2(varint):
    # varint is a byte string in big endian.
    # we need to drop the MSB from each byte and read the number as little endian
    out = 0
    i = 0
    while True:
        try:
            out |= (varint[i] & 0b01111111) << (7 * i)
        except IndexError:
            break
        i += 1
    return out

def get_uint64(filename):
    with open(filename, 'rb') as f:
        unsigned_int = f.read()
    return struct.unpack('>Q', unsigned_int)[0] # big endian

# for i in range(1<<30):
    # assert(decode(encode(i)) == i)
def test1():
    for i in range(1<<25):
        assert(decode1(encode(i)) == i)

def test2():
    for i in range(1<<25):
        assert(decode2(encode(i)) == i)

def wrapper(func):
    def _wrapper():
        func()
    return _wrapper()

print('Decode1:')
cProfile.run('wrapper(test1)')
print('Decode2:')
cProfile.run('wrapper(test2)')

# assert(decode(encode(get_uint64('maxint.uint64'))) == get_uint64('maxint.uint64'))
# assert(decode(encode(get_uint64('150.uint64'))) == get_uint64('150.uint64'))
# assert(decode(encode(get_uint64('1.uint64'))) == get_uint64('1.uint64'))

# Decode1:
#          9404166 function calls in 1.477 seconds

#    Ordered by: standard name

#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    0.000    0.000    1.477    1.477 <string>:1(<module>)
#   1048576    0.544    0.000    0.642    0.000 varint.py:21(decode1)
#   1048576    0.562    0.000    0.642    0.000 varint.py:5(encode)
#         1    0.193    0.193    1.477    1.477 varint.py:55(test1)
#         1    0.000    0.000    1.477    1.477 varint.py:63(wrapper)
#         1    0.000    0.000    1.477    1.477 varint.py:64(_wrapper)
#         1    0.000    0.000    1.477    1.477 {built-in method builtins.exec}
#   4177792    0.098    0.000    0.098    0.000 {built-in method builtins.len}
#   3129216    0.080    0.000    0.080    0.000 {method 'append' of 'list' objects}
#         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


# Decode2:
#          5226374 function calls in 1.354 seconds

#    Ordered by: standard name

#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    0.000    0.000    1.354    1.354 <string>:1(<module>)
#   1048576    0.517    0.000    0.517    0.000 varint.py:35(decode2)
#   1048576    0.571    0.000    0.648    0.000 varint.py:5(encode)
#         1    0.189    0.189    1.354    1.354 varint.py:59(test2)
#         1    0.000    0.000    1.354    1.354 varint.py:63(wrapper)
#         1    0.000    0.000    1.354    1.354 varint.py:64(_wrapper)
#         1    0.000    0.000    1.354    1.354 {built-in method builtins.exec}
#   3129216    0.077    0.000    0.077    0.000 {method 'append' of 'list' objects}
#         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}