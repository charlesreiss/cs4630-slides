#include <stdio.h>
struct pair {
    int a;
    int b;
};

struct pair foo(struct pair w, int x, int y, double z);

void call_example() {
    struct pair argument;
    argument.a = 3;
    argument.b = 4;
    struct pair result = foo(argument, 1, 2, 1.0);
    printf("%d %d\n", result.a, result.b);
}
