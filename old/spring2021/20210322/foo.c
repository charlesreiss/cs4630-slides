#include <stdio.h>
#include <stdlib.h>
int global = 42;
extern int bar;
int main() {
    printf("%d\n", global);
    printf("%p\n", bar);
}
