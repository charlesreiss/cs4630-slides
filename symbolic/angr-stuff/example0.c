#include <stdio.h>
int foo(int a, int b) {
    a += b * 2;
    b *= 4;
    return a + b;
}

int main() {
    int a, b;
    scanf("%d %d", &a, &b);
    printf("%d\n", foo(a, b));
}
