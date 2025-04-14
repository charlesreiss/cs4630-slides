#include <stdio.h>
extern int foo(int);

int main(void) {
    return printf("%d\n", foo(42));
}
