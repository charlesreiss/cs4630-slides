#include <stdio.h>
#include <string.h>

struct Foo {
    virtual void some_method(int size, char *buffer);
};

struct FooAndBuffer {
    char buffer[100];
    Foo *foo;

    FooAndBuffer();
};

void vulnerable() {
    FooAndBuffer danger;
    gets(danger.buffer);
    // ...
    danger.foo->some_method(
        strlen(danger.buffer),
        danger.buffer
    );
}
