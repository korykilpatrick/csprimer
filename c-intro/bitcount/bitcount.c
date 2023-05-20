#include <assert.h>
#include <stdio.h>

unsigned int bitcount(unsigned int n) {
    unsigned int bitcount = 0;
    while (n > 0) {
        if (n & 1) {
            bitcount++;
        }
        n >>= 1;
    }

    return bitcount;
}

int main() {
    assert(bitcount(0) == 0);
    assert(bitcount(1) == 1);
    assert(bitcount(3) == 2);
    assert(bitcount(8) == 1);
    // harder case:
    assert(bitcount(0xffffffff) == 32);
    printf("OK\n");
    return 0;
}
