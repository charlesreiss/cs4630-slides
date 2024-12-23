#include <stdio.h>

__attribute__((noinline))
void do_something_with(const char *p) {
}

void vulnerable() {
    char buffer[100];
    // read string from stdin
    scanf("%s", buffer);

    do_something_with(buffer);
}

int main(void) {
    vulnerable();
    return 0;
}
