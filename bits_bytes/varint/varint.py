# Implementing protobuf varint encoding as detailed https://protobuf.dev/programming-guides/encoding/#varints
import struct 
import cProfile
import time

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

def decode(varint):
    # Drop the MSB from each byte and read the number as little endian
    out = 0
    for i,byte in enumerate(varint):
        out |= (byte & 0b01111111) << (7 * i)
    return out

def get_uint64(filename):
    with open(filename, 'rb') as f:
        unsigned_int = f.read()
    return struct.unpack('>Q', unsigned_int)[0] # big endian

test_data = range(1<<25)
def test():
    for i in test_data:
        assert(decode(encode(i)) == i)

start_time1 = time.perf_counter()
test()
end_time1 = time.perf_counter()
print(f'{end_time1 - start_time1}') # 116.479612671

def wrapper(func):
    def _wrapper():
        func()
    return _wrapper()
cProfile.run('wrapper(test)')

"""         cProfile output
         199212934 function calls in 133.626 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000  133.626  133.626 <string>:1(<module>)
 33554432   43.538    0.000   43.538    0.000 varint.py:19(decode)
        1   15.172   15.172  133.626  133.626 varint.py:32(test)
        1    0.000    0.000  133.626  133.626 varint.py:41(wrapper)
        1    0.000    0.000  133.626  133.626 varint.py:42(_wrapper)
 33554432   64.811    0.000   74.917    0.000 varint.py:6(encode)
        1    0.000    0.000  133.626  133.626 {built-in method builtins.exec}
132104064   10.106    0.000   10.106    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
"""


# print('Decode1:')
# print('Decode2:')
# cProfile.run('wrapper(test2)')
# # Decode1:
#          364871430 function calls in 140.613 seconds

#    Ordered by: standard name

#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    0.000    0.000  140.613  140.613 <string>:1(<module>)
#  33554432   52.357    0.000   63.413    0.000 varint.py:22(decode1)
#         1   12.824   12.824  140.613  140.613 varint.py:54(test1)
#  33554432   55.315    0.000   64.377    0.000 varint.py:6(encode)
#         1    0.000    0.000  140.613  140.613 varint.py:62(wrapper)
#         1    0.000    0.000  140.613  140.613 varint.py:63(_wrapper)
#         1    0.000    0.000  140.613  140.613 {built-in method builtins.exec}
# 165658496   11.056    0.000   11.056    0.000 {built-in method builtins.len}
# 132104064    9.062    0.000    9.062    0.000 {method 'append' of 'list' objects}
#         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


# Decode2:
#          199212934 function calls in 120.128 seconds

#    Ordered by: standard name

#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    0.000    0.000  120.128  120.128 <string>:1(<module>)
#  33554432   44.327    0.000   44.327    0.000 varint.py:36(decode2)
#         1   13.019   13.019  120.128  120.128 varint.py:58(test2)
#  33554432   54.163    0.000   62.782    0.000 varint.py:6(encode)
#         1    0.000    0.000  120.128  120.128 varint.py:62(wrapper)
#         1    0.000    0.000  120.128  120.128 varint.py:63(_wrapper)
#         1    0.000    0.000  120.128  120.128 {built-in method builtins.exec}
# 132104064    8.619    0.000    8.619    0.000 {method 'append' of 'list' objects}
#         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}