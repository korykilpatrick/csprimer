#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <murmurhash.h>
// cc -o hashmap hashmap.c murmurhash.c/murmurhash.c -I murmurhash.c/

#define STARTING_BUCKETS 8
#define MAX_KEY_SIZE 20

typedef struct Node {
  char *key;
  void *value;
  struct Node *next;
} Node;

typedef struct Hashmap {
  unsigned int num_buckets;
  void **buckets;
} Hashmap;

unsigned int hash_to_bucket(char *key, unsigned int num_buckets) {
  uint32_t seed = 0;
  uint32_t bucket = murmurhash(key, (uint32_t) strlen(key), seed) % num_buckets;
  return bucket;
}

Node* Node_new(char *key, void *value) {
  Node* n = malloc(sizeof(Node));
  if (n == NULL) return NULL;

  n->key = strdup(key); // allocates new mem for key
  n->value = value;
  n->next = NULL;
  return n;
}

Hashmap* Hashmap_new(void) {
  Hashmap* h = malloc(sizeof(Hashmap));
  if (h == NULL) return NULL;

  void **buckets = malloc(sizeof(void*) * STARTING_BUCKETS);
  if (buckets == NULL) {
    free(h);
    return NULL;
  }

  h->num_buckets = STARTING_BUCKETS;
  h->buckets = buckets;
  // each bucket will initialize to null
  // the first added node will be the head of a linked list
  for (int i = 0; i < h->num_buckets; i++) {
    buckets[i] = NULL;
  }
  return h;
}

void Hashmap_set(Hashmap* h, char *key, void *value) {
  unsigned int bucket = hash_to_bucket(key, h->num_buckets);
  Node * curr_node = h->buckets[bucket];
  Node * new_node = Node_new(key, value);

  if (curr_node == NULL) {
    h->buckets[bucket] = new_node;
  } else {
    Node * prev_node;
    while (curr_node != NULL) {
      if (strcmp(curr_node->key, key) == 0) {
        printf("Key exists. Value has been updated.\n");
        curr_node->value = value;
        return;
      }
      prev_node = curr_node;
      curr_node = curr_node->next;
    }
    prev_node->next = new_node;
  }
}

void * Hashmap_get(Hashmap * h, char *key) {
  unsigned int bucket = hash_to_bucket(key, h->num_buckets);
  Node *curr_node = h->buckets[bucket];
  while (curr_node != NULL) {
    if (strcmp(curr_node->key, key) == 0) {
      return curr_node->value;
    }
    curr_node = curr_node->next;
  }
  return NULL;
}

void Hashmap_delete(Hashmap *h, char * key) {
  unsigned int bucket = hash_to_bucket(key, h->num_buckets);
  Node *curr_node = h->buckets[bucket];
  Node *prev_node = NULL;
  while (curr_node != NULL) {
    if (strcmp(curr_node->key, key) == 0) {
      if (prev_node == NULL) {
        h->buckets[bucket] = curr_node->next;
      } else {
        prev_node->next = curr_node->next;
      }
      free(curr_node->key);
      free(curr_node);
      break;
    }
    prev_node = curr_node;
    curr_node = curr_node->next;
  }
}

void Hashmap_free(Hashmap *h) {
  for (int b = 0; b < h->num_buckets; b++) {
    Node *curr_node = h->buckets[b];
    Node *next_node;
    while (curr_node != NULL) {
      next_node = curr_node->next;
      free(curr_node->key);
      free(curr_node);
      curr_node = next_node;
    }
  }
  free(h->buckets);
  free(h);
}

void Hashmap_display(Hashmap * h) {
  for (int b = 0; b < h->num_buckets; b++) {
    printf("Bucket %d\n", b);
    Node * curr_node = h->buckets[b];
    while (curr_node != NULL) {
      printf("Key: %s, Value addr: %p\n", curr_node->key, curr_node->value);
      curr_node = curr_node->next;
    }
  }
}

int main() {
  Hashmap *h = Hashmap_new();

  // basic get/set functionality
  int a = 5;
  float b = 7.2;
  Hashmap_set(h, "item a", &a);
  Hashmap_set(h, "item b", &b);
  assert(Hashmap_get(h, "item a") == &a);
  assert(Hashmap_get(h, "item b") == &b);
  // using the same key should override the previous value
  int c = 20;
  Hashmap_set(h, "item a", &c);
  assert(Hashmap_get(h, "item a") == &c);

  // basic delete functionality
  Hashmap_delete(h, "item a");
  assert(Hashmap_get(h, "item a") == NULL);

  // handle collisions correctly
  // note: this doesn't necessarily test expansion
  int i, n = STARTING_BUCKETS * 10, ns[n];
  char key[MAX_KEY_SIZE];
  for (i = 0; i < n; i++) {
    ns[i] = i;
    sprintf(key, "item %d", i);
    Hashmap_set(h, key, &ns[i]);
  }
  Hashmap_display(h);
  for (i = 0; i < n; i++) {
    sprintf(key, "item %d", i);
    assert(Hashmap_get(h, key) == &ns[i]);
  }

  Hashmap_free(h);
  /*
     stretch goals:
     - expand the underlying array if we start to get a lot of collisions
     - support non-string keys
     - try different hash functions
     - switch from chaining to open addressing
     - use a sophisticated rehashing scheme to avoid clustered collisions
     - implement some features from Python dicts, such as reducing space use,
     maintaing key ordering etc. see https://www.youtube.com/watch?v=npw4s1QTmPg
     for ideas
     */
  printf("ok\n");
}
