#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define STARTING_CAPACITY 8

typedef struct DA {
  unsigned int size;
  unsigned int capacity;
  void **array;
} DA;


DA* DA_new (void) {
  DA* da = malloc(sizeof(DA));
  if (da == NULL) return NULL;

  void **array = malloc(sizeof(void*)*STARTING_CAPACITY);
  if (array == NULL) {
    free(da);
    return NULL;
  }

  da->size = 0;
  da->capacity = STARTING_CAPACITY;
  da->array = array;
  return da;
}

int DA_size(DA *da) {
  return da->size;
}

void DA_push (DA* da, void* x) {
  da->array[da->size++] = x;
  if (da->size >= da->capacity) {
    da->capacity *= 2;
    void **new_array = malloc(sizeof(void*) * da->capacity);
    if (new_array == NULL) {
      // Should do some sort of error communication here
      da->size--;
      return;
    }
    memcpy(new_array, da->array, da->size * sizeof(void*));
    free(da->array);
    da->array = new_array;
  }
}

void *DA_pop(DA *da) {
  if (da->size > 0) {
    da->size--;
    return da->array[da->size];
  }
  return NULL;
}

void DA_set(DA *da, void *x, int i) {
  // Supports python-style negative indexing
  if (i < 0) i += da->size;
  if (0 <= i && i < da->size) da->array[i] = x;

  // Do we want to do something with oob indices?
}

void *DA_get(DA *da, int i) {
  if (0 <= i && i < da->size) return da->array[i];
  return NULL;
}


void DA_free(DA *da) {
  free(da->array);
  free(da);
}

int main() {
    DA* da = DA_new();

    assert(DA_size(da) == 0);

    // basic push and pop test
    int x = 5;
    float y = 12.4;
    DA_push(da, &x);
    DA_push(da, &y);
    assert(DA_size(da) == 2);

    assert(DA_pop(da) == &y);
    assert(DA_size(da) == 1);

    assert(DA_pop(da) == &x);
    assert(DA_size(da) == 0);
    assert(DA_pop(da) == NULL);

    // basic set/get test
    DA_push(da, &x);
    DA_set(da, &y, 0);
    assert(DA_get(da, 0) == &y);
    DA_pop(da);
    assert(DA_size(da) == 0);

    // expansion test
    DA *da2 = DA_new(); // use another DA to show it doesn't get overriden
    DA_push(da2, &x);
    int i, n = 100 * STARTING_CAPACITY, arr[n];
    for (i = 0; i < n; i++) {
      arr[i] = i;
      DA_push(da, &arr[i]);
    }
    assert(DA_size(da) == n);
    for (i = 0; i < n; i++) {
      assert(DA_get(da, i) == &arr[i]);
    }
    for (; n; n--)
      DA_pop(da);
    assert(DA_size(da) == 0);
    assert(DA_pop(da2) == &x); // this will fail if da doesn't expand

    DA_free(da);
    DA_free(da2);
    printf("OK\n");
}
