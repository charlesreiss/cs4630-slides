#include <stdio.h>
void one(int unused) {}
void two(int unused) {}

void (*f)(int) = one;

volatile int x;

int foo() {
    f(x);
}

int quux() {
    fprintf(stderr, "Example.");
    return 0;
}

int main() {
    if (x == 1)
        f = two;
    foo();
    quux();
}
