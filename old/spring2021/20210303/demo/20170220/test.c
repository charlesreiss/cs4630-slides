#include <stdio.h>
#include <string.h>
__attribute__((noinline))
void do_calculation(char *something, char *buffer) {
    asm("");
    long value = 0x1234567812345678;
    memcpy(something, &value, sizeof(value));
}

__attribute__((noinline))
void do_something_with(char *something) {
    asm("");
}

struct foo {
    char buffer[8];
    const char *message;
};

__attribute__((noinline))
void process(struct foo* thing) {
    thing->message = "read in process()";
    scanf("%s", thing->buffer);
}


void bar() {
    struct foo thing;
    process(&thing);
    printf("%s: buffer is now %s\n", thing.message, thing.buffer);
}

int main(void) {
    bar();
}
