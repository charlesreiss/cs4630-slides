#include <stdio.h>

void INTERESTING() {
    printf("HERE!\n");
}

void foo(int a, int b) {
  /* (0) */
  if (a != 0) {
    b -= 2;
    a += b;
  }
  /* (1) */
  if (b < 5) {
    b += 4;
  }
  /* (2) */
  if (a + b == 5)
    INTERESTING();
}

int main() {
    int a, b;
    scanf("%d %d", &a, &b);
    foo(a, b);
}
