#include <stdio.h>
#include <stdlib.h>

int min(int a, int b, int c) {
  return a < b ? a < c ? a:c : b;
}

int main() {
  printf("%d\n", min(1,2,3));
  printf("%d\n", min(4,2,3));
  printf("%d\n", min(4,5,3));
  return 0;
}
