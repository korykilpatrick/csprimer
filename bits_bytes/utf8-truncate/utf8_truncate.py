# https://en.wikipedia.org/wiki/UTF-8 for encoding details

def truncate(s, n):
    if len(s) <= n:
        return s
    # find the last byte that is not part of a multi-byte character (i.e. the last byte that does not have the form 10xxxxxx)
    last_byte = n - 1
    if s[last_byte] & 0b10000000 == 0b00000000:
        # last byte is ascii, so we can just return the first n bytes
        return s[:last_byte + 1]
    else:
        # last byte is multi-byte, so we need to find the first byte and return everything before it
        while last_byte >= 0 and (s[last_byte] & 0b11000000) == 0b10000000:
            last_byte -= 1
        return s[:last_byte]

with open('cases', 'rb') as f:
    j = 0
    f2 = open('truncated', 'wb')
    for line in f.readlines():
        n = line[0] # first byte is the target length
        s = line[1:-1] # skip newline char
        truncated = truncate(s, n)
        f2.write(truncated)
        f2.write("\n".encode('utf-8'))

