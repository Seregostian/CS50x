#include <stdio.h>
#include <cs50.h>

/// made it longer so it'd be easier to understand, hope it helps!

int main(void) {
  string name;

  printf("What's your name?\n");

  name = get_string("What's your name?\n", 100);

  printf("Hello, %s!\n", name);

  return 0;
}