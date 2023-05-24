#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

/* TODO: dont need to branch on upper/lower. see Oz vidfor only shifting by lower order 5 bits */
bool ispangram(char *s) {
  // create a 26 bit mask, return true if mask is full
  unsigned int mask = 0;
  while (*s != '\0' && mask < (1 << 26) - 1) {
    int ascii_val = (int) *s;
    if (ascii_val >= 65 && ascii_val <= 90) {
      // uppercase letters
      mask = mask | (1 << (ascii_val - 65));
    }
    else if (ascii_val >= 97 && ascii_val <= 122) {
      // lowercase letters
      mask = mask | (1 << (ascii_val - 97));
    }
    s++;
  }
  return mask == (1 << 26) - 1;
}

int main() {
  size_t len;
  ssize_t read;
  char *line = NULL;
  while ((read = getline(&line, &len, stdin)) != -1) {
    if (ispangram(line))
      printf("%s", line);
  }

  if (ferror(stdin))
    fprintf(stderr, "Error reading from stdin");

  free(line);
  fprintf(stderr, "ok\n");
}
